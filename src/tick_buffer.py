# tick_buffer.py — Phase 1 tick buffer, Parquet storage and replay (T-002)

"""
Raw L2 tick retention and deterministic replay.

The buffer accepts ticks from :mod:`src.fast_l2_client`, keeps them in a
bounded in-memory block, and flushes that block to Parquet.  Nothing is
transformed: every field of :class:`~src.fast_l2_client.L2Tick` survives the
round trip, including full level order and quantities (docs/DataSpec.md).

Guarantees (docs/TaskQueue.md T-002):

* **Complete fields.**  symbol, all bid/ask levels (price and quantity),
  ``ts_exchange_ns``, ``ts_local_ns``, ``seq`` and the tick quantum
  ``tick_index`` are stored and restored exactly.
* **Ordering.**  ``tick_index`` must be strictly increasing inside a
  dataset; a regression raises :class:`TickOrderError` instead of silently
  reordering.  Replay returns ticks in ``(tick_index)`` order, so the same
  dataset always yields the same sequence.
* **No corruption.**  Coverage is anchored on a single writer per partition
  (``part-*.parquet``), so replay never depends on filesystem order.
* **Offline.**  Storage and replay touch only local files, so physics,
  detector and simulation tests can run without a socket.

Layout (docs/DataSpec.md §Storage)::

    <root>/symbol=BTCUSDT/day=2026-10-11/part-0001.parquet

Parquet + zstd, written with ``polars`` (docs/Implementation.md §2,
docs/TaskQueue.md T-002).  One row per tick; level arrays are stored as
variable-length ``List(Float64)`` columns.

Usage::

    store  = L2ParquetStore("data/l2")
    buffer = TickBuffer(store, flush_rows=50_000)
    buffer.append(tick)                 # auto-flushes when full
    buffer.flush()

    replay = TickReplay("data/l2")
    for tick in replay.ticks():         # deterministic order
        ...
    for state in replay.states():       # feeds src.physics_jax.state_from_l2
        ...

No derived quantities are stored: the dataset is the raw record, and every
model quantity is recomputed at replay time (docs/goal.md, Axiom 1).
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, Sequence, Tuple

import polars as pl

from src.fast_l2_client import L2Tick

# Column order is frozen: Parquet readers rely on it for deterministic output.
LEVEL_COLUMNS = ("bid_prices", "bid_quantities", "ask_prices", "ask_quantities")
SCALAR_COLUMNS = ("tick_index", "symbol", "seq", "ts_exchange_ns", "ts_local_ns")
TICK_SCHEMA: Dict[str, pl.DataType] = {
    "tick_index": pl.Int64(),
    "symbol": pl.Utf8(),
    "seq": pl.Int64(),
    "ts_exchange_ns": pl.Int64(),
    "ts_local_ns": pl.Int64(),
    "bid_prices": pl.List(pl.Float64()),
    "bid_quantities": pl.List(pl.Float64()),
    "ask_prices": pl.List(pl.Float64()),
    "ask_quantities": pl.List(pl.Float64()),
}

_PART_RE = re.compile(r"part-(\d+)\.parquet$")


class TickOrderError(ValueError):
    """Raised when a tick is appended out of order (ordering guarantee)."""


def _day_of(ts_local_ns: int) -> str:
    """UTC calendar day of a local timestamp, ``YYYY-MM-DD`` (DataSpec partition)."""
    seconds = int(ts_local_ns) // 1_000_000_000
    return _dt.datetime.fromtimestamp(seconds, tz=_dt.timezone.utc).strftime("%Y-%m-%d")


def tick_to_row(tick: L2Tick) -> dict:
    """Flatten one tick into a Parquet row, preserving level order verbatim."""
    bid_prices = [p for p, _ in tick.bids]
    bid_quantities = [q for _, q in tick.bids]
    ask_prices = [p for p, _ in tick.asks]
    ask_quantities = [q for _, q in tick.asks]
    return {
        "tick_index": int(tick.tick_index),
        "symbol": str(tick.symbol),
        "seq": int(tick.seq),
        "ts_exchange_ns": int(tick.ts_exchange_ns),
        "ts_local_ns": int(tick.ts_local_ns),
        "bid_prices": bid_prices,
        "bid_quantities": bid_quantities,
        "ask_prices": ask_prices,
        "ask_quantities": ask_quantities,
    }


def row_to_tick(row: dict) -> L2Tick:
    """Rebuild a tick from one stored row (exact inverse of ``tick_to_row``)."""
    bids = tuple(zip(row["bid_prices"] or (), row["bid_quantities"] or ()))
    asks = tuple(zip(row["ask_prices"] or (), row["ask_quantities"] or ()))
    return L2Tick(
        symbol=row["symbol"],
        bids=bids,
        asks=asks,
        seq=int(row["seq"]),
        ts_exchange_ns=int(row["ts_exchange_ns"]),
        ts_local_ns=int(row["ts_local_ns"]),
        tick_index=int(row["tick_index"]),
    )


@dataclass
class StoreStats:
    """Counters for the storage layer (used by tests and the research log)."""

    written: int = 0
    files: int = 0
    flushes: int = 0


class L2ParquetStore:
    """Append-only Parquet store, partitioned by ``symbol`` and UTC ``day``.

    Each partition directory holds one file per flush, and part numbers are
    allocated from the existing directory contents so a reopened store never
    overwrites previously written data.
    """

    def __init__(self, root: str | Path, *, compression: str = "zstd") -> None:
        self.root = Path(root)
        self.compression = compression
        self.stats = StoreStats()

    # -- paths --------------------------------------------------------

    def partition_dir(self, symbol: str, day: str) -> Path:
        return self.root / f"symbol={symbol.upper()}" / f"day={day}"

    def _next_part(self, directory: Path) -> Path:
        highest = 0
        if directory.exists():
            for path in directory.glob("part-*.parquet"):
                match = _PART_RE.search(path.name)
                if match:
                    highest = max(highest, int(match.group(1)))
        return directory / f"part-{highest + 1:04d}.parquet"

    # -- writing ------------------------------------------------------

    def write(self, ticks: Sequence[L2Tick]) -> list[Path]:
        """Write ``ticks`` grouped by partition; return the files written.

        Rows are ordered by ``tick_index`` inside each file.  Partitions for
        the same ``(symbol, day)`` in one call are coalesced into one file.
        """
        if not ticks:
            return []

        grouped: Dict[Tuple[str, str], list[L2Tick]] = {}
        for tick in ticks:
            grouped.setdefault((tick.symbol.upper(), _day_of(tick.ts_local_ns)),
                               []).append(tick)

        written: list[Path] = []
        for (symbol, day), chunk in sorted(grouped.items()):
            rows = [tick_to_row(t) for t in sorted(chunk, key=lambda t: t.tick_index)]
            frame = pl.DataFrame(rows, schema=TICK_SCHEMA)
            directory = self.partition_dir(symbol, day)
            directory.mkdir(parents=True, exist_ok=True)
            path = self._next_part(directory)
            frame.write_parquet(path, compression=self.compression)
            written.append(path)
            self.stats.written += len(rows)
            self.stats.files += 1
            self.stats.flushes += 1
        return written

    # -- reading ------------------------------------------------------

    def files(self, *, symbols: Iterable[str] | None = None,
              days: Iterable[str] | None = None) -> list[Path]:
        """All partition files, deterministically ordered."""
        wanted_symbols = {s.upper() for s in symbols} if symbols else None
        wanted_days = set(days) if days else None

        found: list[Path] = []
        if not self.root.exists():
            return found
        for symbol_dir in sorted(self.root.glob("symbol=*")):
            symbol = symbol_dir.name.split("=", 1)[1]
            if wanted_symbols is not None and symbol not in wanted_symbols:
                continue
            for day_dir in sorted(symbol_dir.glob("day=*")):
                day = day_dir.name.split("=", 1)[1]
                if wanted_days is not None and day not in wanted_days:
                    continue
                for path in sorted(day_dir.glob("part-*.parquet")):
                    found.append(path)
        return found

    def read_rows(self, **filters) -> Iterator[dict]:
        """Yield stored rows in deterministic partition/part order."""
        for path in self.files(**filters):
            frame = pl.read_parquet(path)
            for row in frame.iter_rows(named=True):
                yield row


class TickBuffer:
    """Bounded in-memory tick block that flushes to an :class:`L2ParquetStore`.

    The block is bounded by ``flush_rows``: reaching it triggers a write, so
    memory stays finite (docs/Implementation.md §5, "unbounded memory").
    """

    def __init__(self, store: L2ParquetStore, *, flush_rows: int = 50_000) -> None:
        if flush_rows < 1:
            raise ValueError("flush_rows must be >= 1")
        self.store = store
        self.flush_rows = int(flush_rows)
        self._block: list[L2Tick] = []
        self._last_index: int | None = None
        self.stats = StoreStats()

    def __len__(self) -> int:
        return len(self._block)

    @property
    def pending(self) -> int:
        return len(self._block)

    def append(self, tick: L2Tick) -> list[Path]:
        """Append one tick; flush when the block is full.  Returns new files.

        Raises
        ------
        TickOrderError
            If ``tick.tick_index`` does not strictly increase, so a dataset
            can never be stored out of order.
        """
        if self._last_index is not None and tick.tick_index <= self._last_index:
            raise TickOrderError(
                f"tick_index {tick.tick_index} after {self._last_index}; "
                "a dataset must be stored in strictly increasing tick order"
            )
        self._last_index = tick.tick_index
        self._block.append(tick)
        if len(self._block) >= self.flush_rows:
            return self.flush()
        return []

    def extend(self, ticks: Iterable[L2Tick]) -> list[Path]:
        written: list[Path] = []
        for tick in ticks:
            written.extend(self.append(tick))
        return written

    def flush(self) -> list[Path]:
        """Write the pending block (if any) and clear it."""
        if not self._block:
            return []
        block, self._block = self._block, []
        paths = self.store.write(block)
        self.stats.written += len(block)
        self.stats.flushes += 1
        self.stats.files += len(paths)
        return paths

    def __enter__(self) -> "TickBuffer":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.flush()


class TickReplay:
    """Deterministic replay of a stored dataset.

    ``ticks()`` yields every stored tick in ``tick_index`` order (across
    partitions).  ``states()`` aligns the three assets and yields a
    :class:`~src.physics_jax.ThreeBodyState` per tick, using the latest
    snapshot of each asset — one L2 update is one tick (docs/TickModel.md).
    The first states are withheld until all three assets have a book, so the
    emitted series never contains an undefined body.

    Parameters
    ----------
    state_symbols : Sequence[str]
        The three assets that form the three-body state, in body order.
    symbols, days : optional iterables
        Read filters (DataSpec.md partitions).  ``symbols`` also accepts a
        single-symbol selection for ``ticks()``; ``states()`` additionally
        requires ``state_symbols`` to be present in the data.
    """

    def __init__(self, root_or_store: str | Path | L2ParquetStore, *,
                 state_symbols: Sequence[str] = ("BTCUSDT", "ETHUSDT", "SOLUSDT"),
                 symbols: Iterable[str] | None = None,
                 days: Iterable[str] | None = None) -> None:
        self.store = (root_or_store if isinstance(root_or_store, L2ParquetStore)
                      else L2ParquetStore(root_or_store))
        self.symbols = tuple(s.upper() for s in state_symbols)
        self.filters: dict = {}
        if symbols is not None:
            self.filters["symbols"] = list(symbols)
        if days is not None:
            self.filters["days"] = list(days)

    # -- raw ticks ----------------------------------------------------

    def ticks(self) -> Iterator[L2Tick]:
        """All stored ticks, ordered by ``tick_index`` (ties keep file order)."""
        rows = list(self.store.read_rows(**self.filters))
        rows.sort(key=lambda row: (int(row["tick_index"]),
                                   str(row["symbol"])))
        for row in rows:
            yield row_to_tick(row)

    def ticks_by_symbol(self) -> Dict[str, list[L2Tick]]:
        """Per-symbol tick lists, each in ``tick_index`` order."""
        grouped: Dict[str, list[L2Tick]] = {}
        for tick in self.ticks():
            grouped.setdefault(tick.symbol, []).append(tick)
        return grouped

    # -- physics hand-off ---------------------------------------------

    def states(self) -> Iterator["object"]:
        """Yield a ``ThreeBodyState`` per tick once all assets have a book.

        Feeds ``src.physics_jax.state_from_l2`` with the current snapshot of
        each of the three assets (latest-wins), which is exactly the tick
        semantics of docs/TickModel.md.
        """
        from src.physics_jax import state_from_l2  # local import: JAX is heavy

        latest: Dict[str, L2Tick] = {}
        for tick in self.ticks():
            latest[tick.symbol] = tick
            if all(symbol in latest for symbol in self.symbols):
                books = [latest[symbol] for symbol in self.symbols]
                yield state_from_l2(
                    _levels_array(books[0].bids), _levels_array(books[0].asks),
                    _levels_array(books[1].bids), _levels_array(books[1].asks),
                    _levels_array(books[2].bids), _levels_array(books[2].asks),
                )


def _levels_array(levels: Sequence[Tuple[float, float]]):
    """Convert stored level tuples to the ``(K, 2)`` array physics_jax expects."""
    import jax.numpy as jnp

    if not levels:
        return jnp.zeros((0, 2))
    return jnp.asarray(levels, dtype=jnp.float64)


def replay_summary(store: L2ParquetStore, **filters) -> dict:
    """Counters that make a stored dataset auditable without loading JAX."""
    counts: Dict[str, int] = {}
    total = 0
    first_index: int | None = None
    last_index: int | None = None
    for row in store.read_rows(**filters):
        symbol = str(row["symbol"])
        counts[symbol] = counts.get(symbol, 0) + 1
        index = int(row["tick_index"])
        first_index = index if first_index is None else min(first_index, index)
        last_index = index if last_index is None else max(last_index, index)
        total += 1
    return {
        "total": total,
        "per_symbol": counts,
        "first_tick_index": first_index,
        "last_tick_index": last_index,
    }


# ---------------------------------------------------------------------
# Minimal Parquet footer reader (no extra dependency)
# ---------------------------------------------------------------------
# DataSpec.md §Storage prescribes zstd.  The codec is stored as a Thrift
# *enum* inside the footer, so it is not visible as a string in the file and
# reading it normally needs pyarrow.  Rather than add a heavy dependency (or
# make a weak "the file got smaller" argument), the store exposes a tiny
# reader for the footer's ColumnMetaData.codec field.  Only the few fields
# needed for that are decoded; everything else is skipped.

_CODEC_NAMES = {0: "UNCOMPRESSED", 1: "SNAPPY", 2: "GZIP", 3: "LZO",
                4: "BROTLI", 5: "LZ4", 6: "ZSTD", 7: "LZ4_RAW"}

_CT_STOP, _CT_TRUE, _CT_FALSE, _CT_BYTE, _CT_I16, _CT_I32, _CT_I64, \
    _CT_DOUBLE, _CT_BINARY, _CT_LIST, _CT_SET, _CT_MAP, _CT_STRUCT = range(13)


class _ThriftReader:
    """Just enough Thrift compact-protocol to walk the Parquet footer."""

    def __init__(self, buf: bytes, pos: int = 0) -> None:
        self.buf = buf
        self.pos = pos
        self.last_field = 0

    def _byte(self) -> int:
        value = self.buf[self.pos]
        self.pos += 1
        return value

    def _varint(self) -> int:
        shift = 0
        result = 0
        while True:
            byte = self._byte()
            result |= (byte & 0x7F) << shift
            if not byte & 0x80:
                return result
            shift += 7

    def _zigzag(self) -> int:
        raw = self._varint()
        return (raw >> 1) ^ -(raw & 1)

    def struct_fields(self) -> Iterator[tuple[int, int]]:
        """Yield ``(field_type, field_id)`` until the struct terminator.

        Field-id deltas are relative to the enclosing struct only, so the
        parent's position is saved and restored around nested parsing
        (either explicit decoding or :meth:`skip`).
        """
        saved = self.last_field
        self.last_field = 0
        try:
            while True:
                header = self._byte()
                if header == _CT_STOP:
                    return
                ftype = header & 0x0F
                delta = header >> 4
                if delta:
                    self.last_field += delta
                else:
                    self.last_field = self._zigzag()
                yield ftype, self.last_field
        finally:
            self.last_field = saved

    def read_i32(self) -> int:
        return self._zigzag()

    def read_i64(self) -> int:
        return self._zigzag()

    def read_binary(self) -> bytes:
        length = self._varint()
        value = self.buf[self.pos:self.pos + length]
        self.pos += length
        return value

    def read_list_header(self) -> tuple[int, int]:
        header = self._byte()
        size = header >> 4
        etype = header & 0x0F
        if size == 15:
            size = self._varint()
        return etype, size

    def skip(self, ftype: int) -> None:
        if ftype in (_CT_TRUE, _CT_FALSE):
            return
        if ftype == _CT_BYTE:
            self.pos += 1
        elif ftype in (_CT_I16, _CT_I32, _CT_I64):
            self._varint()
        elif ftype == _CT_DOUBLE:
            self.pos += 8
        elif ftype == _CT_BINARY:
            self.read_binary()
        elif ftype in (_CT_LIST, _CT_SET):
            etype, size = self.read_list_header()
            for _ in range(size):
                self.skip(etype)
        elif ftype == _CT_MAP:
            size = self._varint()
            if size:
                header = self._byte()
                for _ in range(size):
                    self.skip(header >> 4)
                    self.skip(header & 0x0F)
        elif ftype == _CT_STRUCT:
            for child_type, _ in self.struct_fields():
                self.skip(child_type)

    def skip_struct(self) -> None:
        for ftype, _ in self.struct_fields():
            self.skip(ftype)


def parquet_codecs(path: str | Path) -> list[str]:
    """Codec name of every column chunk in a Parquet file (DataSpec.md §Storage).

    Returns e.g. ``["ZSTD", "ZSTD", ...]``; unknown enum values are returned
    as ``"UNKNOWN(<n>)"`` so a schema change cannot silently pass.
    """
    data = Path(path).read_bytes()
    if data[:4] != b"PAR1" or data[-4:] != b"PAR1":
        raise ValueError(f"not a Parquet file: {path}")
    footer_len = int.from_bytes(data[-8:-4], "little")
    footer = data[-8 - footer_len:-8]

    reader = _ThriftReader(footer)
    codecs: list[str] = []
    for ftype, field_id in reader.struct_fields():          # FileMetaData
        if field_id == 4 and ftype == _CT_LIST:             # row_groups
            _, n_groups = reader.read_list_header()
            for _ in range(n_groups):
                for rg_type, rg_id in reader.struct_fields():   # RowGroup
                    if rg_id == 1 and rg_type == _CT_LIST:      # columns
                        _, n_chunks = reader.read_list_header()
                        for _ in range(n_chunks):
                            codecs.append(_column_codec(reader))
                    else:
                        reader.skip(rg_type)
        else:
            reader.skip(ftype)
    return codecs


def _column_codec(reader: _ThriftReader) -> str:            # ColumnChunk
    codec = -1
    for ftype, field_id in reader.struct_fields():
        if field_id == 3 and ftype == _CT_STRUCT:           # meta_data
            for md_type, md_id in reader.struct_fields():   # ColumnMetaData
                if md_id == 4 and md_type == _CT_I32:       # codec
                    codec = reader.read_i32()
                else:
                    reader.skip(md_type)
        else:
            reader.skip(ftype)
    return _CODEC_NAMES.get(codec, f"UNKNOWN({codec})")


__all__ = [
    "L2ParquetStore",
    "StoreStats",
    "TICK_SCHEMA",
    "TickBuffer",
    "TickOrderError",
    "TickReplay",
    "parquet_codecs",
    "replay_summary",
    "row_to_tick",
    "tick_to_row",
]
