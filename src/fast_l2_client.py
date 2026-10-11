# fast_l2_client.py — Phase 1 raw L2 tick ingestion (T-001)

"""
Fast L2 tick client: raw WebSocket ingestion of order-book snapshots.

The client is deliberately *dumb*: it connects, decodes JSON, preserves the
raw bid/ask levels exactly as the exchange sent them, and hands the ticks to
the consumer in arrival order.  It performs no aggregation, no filtering, no
indicator calculation and no physics.  Those belong to later phases.

Design rules (docs/TaskQueue.md T-001, docs/goal.md, docs/DataSpec.md):

* Only raw L2 tick data.  20 levels per side, exactly what the feed carries.
* No external parameters.  The only configuration is what is required to
  connect: endpoint URL, asset symbols and the stream rate (DataSpec.md
  ``depth20@100ms``).  Nothing here influences the physics model.
* Time is quantised in ticks (docs/TickModel.md): one tick = one L2 update.
  ``tick_index`` is that quantum, assigned in arrival order.
* No drops.  ``stream()`` is a pull generator, so a slow consumer pauses the
  reader instead of losing ticks; the optional driver queue is bounded and
  its puts block.  ``stats.dropped`` stays 0 by construction and is checked
  by the acceptance test.
* ADR-004 (uvloop + orjson) is honoured *where applicable*.  uvloop has no
  Windows implementation and orjson is optional, so both are used when
  importable and both degrade to the standard library otherwise.  See
  docs/Decisions.md ADR-010.

Validation rules from docs/DataSpec.md:

* bids strictly descending, asks strictly ascending
* best_bid < best_ask
* all volumes > 0

Violations are *counted* (``TickStats.invalid_books``), never repaired and
never used to drop a tick: silently fixing the book would be a filter.  A
violation is a falsifiability signal (docs/Falsifiability.md F2, jump to
zero depth).

Usage::

    client = FastL2Client()
    async for tick in client.stream():          # pull-driven
        buffer.append(tick)

    await client.start()                        # driver-loop style
    ticks = await client.pop_batch(512)         # docs/Implementation.md §4
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import sys
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator, Awaitable, Callable, Iterable, Sequence, Tuple

# ---------------------------------------------------------------------
# Optional accelerator imports (ADR-004: uvloop + orjson, where applicable)
# ---------------------------------------------------------------------

try:  # orjson is the ADR-004 JSON decoder; stdlib json is byte-equivalent.
    import orjson as _orjson
except ImportError:  # pragma: no cover - depends on the environment
    _orjson = None

HAS_ORJSON: bool = _orjson is not None

HAS_UVLOOP: bool = False
_uvloop = None
if sys.platform != "win32":  # uvloop has no Windows support
    try:  # pragma: no cover - platform dependent
        import uvloop as _uvloop

        HAS_UVLOOP = True
    except ImportError:
        _uvloop = None


def install_event_loop_policy() -> str:
    """Install uvloop when available, else keep the stdlib asyncio policy.

    ADR-004 asks for uvloop.  uvloop is POSIX-only, so on Windows this is a
    no-op.  Returns the name of the policy actually installed (``"uvloop"``
    or ``"asyncio"``) so callers can log which one is active.
    """
    if HAS_UVLOOP:  # pragma: no cover - platform dependent
        asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())
        return "uvloop"
    return "asyncio"


# ---------------------------------------------------------------------
# Feed definition — every value below is traceable to a document
# ---------------------------------------------------------------------

BINANCE_WS_BASE = "wss://stream.binance.com:9443/stream"

# Market-data-only domain for the same streams.  In several regions the main
# domain answers HTTP 451 (Unavailable For Legal Reasons) for order-book
# streams; the .vision endpoint serves the identical `depth20@100ms` payloads.
# Measured 2026-10-11: main domain 451, .vision streaming normally (see
# docs/ResearchLog.md).  This is a connection parameter only — no model input.
BINANCE_WS_BASE_ALT = "wss://data-stream.binance.vision/stream"

# Three assets of the mission (docs/MISSION_PROMPT.md §1): BTC, ETH, SOL.
DEFAULT_SYMBOLS: Tuple[str, ...] = ("btcusdt", "ethusdt", "solusdt")

# DataSpec.md §L2 Schema: depth20 snapshot every 100 ms.
DEFAULT_LEVELS = 20
DEFAULT_RATE_MS = 100


def stream_names(symbols: Sequence[str] = DEFAULT_SYMBOLS,
                 levels: int = DEFAULT_LEVELS,
                 rate_ms: int = DEFAULT_RATE_MS) -> list[str]:
    """Build the combined-stream names, e.g. ``btcusdt@depth20@100ms``."""
    return [f"{s.lower()}@depth{levels}@{rate_ms}ms" for s in symbols]


def stream_url(symbols: Sequence[str] = DEFAULT_SYMBOLS,
               levels: int = DEFAULT_LEVELS,
               rate_ms: int = DEFAULT_RATE_MS,
               base: str = BINANCE_WS_BASE) -> str:
    """Combined-stream URL for the three assets (raw snapshots, not diffs)."""
    return f"{base}?streams={'/'.join(stream_names(symbols, levels, rate_ms))}"


def _loads(raw: Any) -> Any:
    """Decode one JSON message (orjson when present, stdlib json otherwise)."""
    if _orjson is not None:
        return _orjson.loads(raw)
    if isinstance(raw, (bytes, bytearray, memoryview)):
        raw = bytes(raw).decode("utf-8")
    return json.loads(raw)


def _levels(raw_levels: Iterable[Sequence[Any]]) -> Tuple[Tuple[float, float], ...]:
    """Keep levels exactly as received: ``[price, quantity]`` pairs, in order.

    No sorting, no aggregation, no zero-level removal — that would be a
    filter (docs/goal.md).
    """
    return tuple((float(level[0]), float(level[1])) for level in raw_levels)


@dataclass(frozen=True)
class L2Tick:
    """One raw L2 update — one tick (docs/TickModel.md, docs/DataSpec.md).

    Attributes
    ----------
    symbol : str
        Upper-case asset symbol, e.g. ``"BTCUSDT"``.
    bids, asks : tuple[tuple[float, float], ...]
        ``(price, quantity)`` levels in exchange order, best level first.
    seq : int
        Exchange sequence number (``lastUpdateId``); 0 when absent.
    ts_exchange_ns : int
        Exchange event time in nanoseconds; 0 when the stream carries none
        (the ``depth20`` snapshot payload has no ``E`` field).
    ts_local_ns : int
        Local receive time in nanoseconds (from the injected clock).
    tick_index : int
        Arrival ordinal — the tick quantum (docs/TickModel.md).
    """

    symbol: str
    bids: Tuple[Tuple[float, float], ...]
    asks: Tuple[Tuple[float, float], ...]
    seq: int
    ts_exchange_ns: int
    ts_local_ns: int
    tick_index: int

    @property
    def best_bid(self) -> float:
        return self.bids[0][0] if self.bids else 0.0

    @property
    def best_ask(self) -> float:
        return self.asks[0][0] if self.asks else 0.0

    def is_well_formed(self) -> bool:
        """docs/DataSpec.md validation rules, as a pure predicate.

        ``bids`` strictly descending, ``asks`` strictly ascending,
        ``best_bid < best_ask``, all volumes > 0.  An empty side is *not*
        well-formed, but it is not rejected either — zero depth is the
        self-freeze case the physics must survive (docs/Falsifiability.md F2).
        """
        if not self.bids or not self.asks:
            return False
        if any(q <= 0.0 for _, q in self.bids + self.asks):
            return False
        if any(self.bids[i][0] <= self.bids[i + 1][0]
               for i in range(len(self.bids) - 1)):
            return False
        if any(self.asks[i][0] >= self.asks[i + 1][0]
               for i in range(len(self.asks) - 1)):
            return False
        return self.best_bid < self.best_ask


def parse_message(raw: Any,
                  *,
                  ts_local_ns: int,
                  tick_index: int,
                  default_symbol: str | None = None) -> L2Tick:
    """Decode one raw feed message into an :class:`L2Tick`.  Pure function.

    Handles the combined-stream envelope (``{"stream": ..., "data": {...}}``,
    docs/DataSpec.md) and the bare payload.  Level order and quantities are
    preserved verbatim.
    """
    msg = _loads(raw)
    if not isinstance(msg, dict):
        raise ValueError(f"not a JSON object: {msg!r}")

    if "data" in msg and "stream" in msg:
        payload = msg["data"]
        symbol = str(msg["stream"]).split("@", 1)[0].upper()
    elif "bids" in msg and "asks" in msg:
        payload = msg
        if default_symbol is None:
            raise ValueError("bare payload without symbol and no default_symbol")
        symbol = default_symbol.upper()
    else:
        raise ValueError(f"unrecognised L2 message: {msg!r}")

    bids = _levels(payload.get("bids") or ())
    asks = _levels(payload.get("asks") or ())

    event_ms = payload.get("E")      # present on diff-depth, absent on depth20
    ts_exchange_ns = int(event_ms) * 1_000_000 if event_ms is not None else 0

    return L2Tick(
        symbol=symbol,
        bids=bids,
        asks=asks,
        seq=int(payload.get("lastUpdateId", 0) or 0),
        ts_exchange_ns=ts_exchange_ns,
        ts_local_ns=int(ts_local_ns),
        tick_index=int(tick_index),
    )


# ---------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------

@asynccontextmanager
async def _websockets_connector(url: str, open_timeout: float) -> AsyncIterator[Any]:
    """Default transport: ``websockets`` client (new API, legacy fallback)."""
    try:  # websockets >= 13
        from websockets.asyncio.client import connect as _connect
    except ImportError:  # pragma: no cover - older websockets
        from websockets.client import connect as _connect  # type: ignore

    async with _connect(url, open_timeout=open_timeout, max_size=None,
                        ping_interval=20.0, ping_timeout=20.0) as ws:
        yield ws


Connector = Callable[[str, float], Any]
"""``connector(url, open_timeout)`` → async context manager yielding a socket."""


@dataclass
class TickStats:
    """Bookkeeping for the T-001 no-drop / ordering exit criteria."""

    received: int = 0        # decoded messages
    delivered: int = 0       # ticks handed to a consumer
    dropped: int = 0         # ticks lost to queue overflow (must stay 0)
    out_of_order: int = 0    # per-symbol sequence regressions (must stay 0)
    invalid_books: int = 0   # docs/DataSpec.md validation failures (informational)
    reconnects: int = 0
    last_error: str | None = None   # why the last reconnect happened

    def as_dict(self) -> dict:
        return {
            "received": self.received,
            "delivered": self.delivered,
            "dropped": self.dropped,
            "out_of_order": self.out_of_order,
            "invalid_books": self.invalid_books,
            "reconnects": self.reconnects,
            "last_error": self.last_error,
        }


# ---------------------------------------------------------------------
# The client
# ---------------------------------------------------------------------

class FastL2Client:
    """Raw L2 snapshot client for the three assets, in order, without drops.

    Parameters
    ----------
    symbols : Sequence[str]
        Asset symbols (default: the mission's BTC/ETH/SOL).
    levels, rate_ms : int
        Snapshot depth and cadence, fixed by docs/DataSpec.md.
    url : str, optional
        Override the endpoint (used by tests and the mock server).
    connector : callable, optional
        Transport factory ``connector(url, open_timeout)``; defaults to
        ``websockets``.  Injecting it keeps tests offline.
    clock : callable, optional
        Nanosecond clock ``clock() -> int`` (default ``time.time_ns``);
        injectable so tests stay deterministic.
    queue_size : int
        Bounded driver queue (``start()``/``pop_batch()`` mode).  Puts block,
        so a slow consumer applies back-pressure instead of losing ticks.
    reconnect_delay_s : float
        Delay before reconnecting after a transport failure.  Purely a
        connection parameter; it never influences tick content.
    max_reconnects : int, optional
        Stop after this many consecutive transport failures
        (``None`` = retry forever).
    """

    def __init__(
        self,
        symbols: Sequence[str] = DEFAULT_SYMBOLS,
        *,
        levels: int = DEFAULT_LEVELS,
        rate_ms: int = DEFAULT_RATE_MS,
        url: str | None = None,
        connector: Connector | None = None,
        clock: Callable[[], int] = time.time_ns,
        queue_size: int = 8192,
        open_timeout: float = 10.0,
        reconnect_delay_s: float = 1.0,
        max_reconnects: int | None = None,
    ) -> None:
        self.symbols = tuple(s.upper() for s in symbols)
        self.url = url or stream_url(symbols, levels, rate_ms)
        self.connector = connector or _websockets_connector
        self.clock = clock
        self.queue_size = int(queue_size)
        self.open_timeout = float(open_timeout)
        self.reconnect_delay_s = float(reconnect_delay_s)
        self.max_reconnects = max_reconnects

        self.stats = TickStats()
        self._queue: asyncio.Queue[L2Tick | None] = asyncio.Queue(self.queue_size)
        self._producer: asyncio.Task | None = None
        self._tick_index = 0
        self._last_seq: dict[str, int] = {}
        self._closed = False

    # -- ingestion ----------------------------------------------------

    def _ingest(self, raw: Any) -> L2Tick:
        """Decode, order-check and account for one raw message."""
        tick = parse_message(raw, ts_local_ns=self.clock(),
                             tick_index=self._tick_index)

        previous = self._last_seq.get(tick.symbol)
        if previous is not None and tick.seq < previous:
            self.stats.out_of_order += 1
        self._last_seq[tick.symbol] = tick.seq

        # The snapshot cadence is 100 ms, so ``lastUpdateId`` advances in
        # jumps between ticks: a seq *gap* is not a drop, only a regression
        # is an ordering violation.
        if not tick.is_well_formed():
            self.stats.invalid_books += 1

        self._tick_index += 1
        self.stats.received += 1
        return tick

    # -- streaming (pull semantics: a slow consumer slows the reader) --

    async def stream(self) -> AsyncIterator[L2Tick]:
        """Yield raw ticks in arrival order until the caller stops.

        Transport failures trigger a reconnect; decoded ticks are never
        discarded and nothing blocks the event loop.

        The generator owns the socket, so a consumer that stops early must
        close it explicitly — ``contextlib.aclosing(client.stream())`` — or use
        :meth:`run`, which does that for you.
        """
        failures = 0
        while not self._closed:
            try:
                async with self.connector(self.url, self.open_timeout) as socket:
                    async for raw in socket:
                        tick = self._ingest(raw)
                        self.stats.delivered += 1
                        yield tick
                    return  # clean end of a finite stream
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                # Never lose decoded ticks, but never hide the reason either:
                # the failure is recorded so a silent retry loop stays
                # diagnosable (observability, docs/QA_Protocol.md).
                failures += 1
                self.stats.last_error = f"{type(exc).__name__}: {exc}"
                if (self.max_reconnects is not None
                        and failures > self.max_reconnects):
                    raise
                self.stats.reconnects += 1
                await asyncio.sleep(self.reconnect_delay_s)

    async def run(self, consumer: Callable[[L2Tick], Awaitable[None] | None],
                  *, limit: int | None = None) -> int:
        """Drive ``consumer`` for every tick; return the number consumed.

        ``limit`` stops after that many ticks (the 100 000-tick acceptance
        run and the offline tests).
        """
        count = 0
        # aclosing() runs the stream generator's finally on early break, so a
        # bounded run never leaves a socket half-open or a task dangling.
        async with contextlib.aclosing(self.stream()) as ticks:
            async for tick in ticks:
                result = consumer(tick)
                if result is not None:
                    await result
                count += 1
                if limit is not None and count >= limit:
                    break
        return count

    # -- driver-loop mode (docs/Implementation.md §4) ------------------

    async def start(self) -> None:
        """Start the background reader feeding the bounded queue."""
        if self._producer is None or self._producer.done():
            self._producer = asyncio.create_task(self._produce())

    async def _produce(self) -> None:
        try:
            async for tick in self.stream():
                await self._queue.put(tick)   # blocks: back-pressure, no drop
        finally:
            await self._queue.put(None)

    async def pop_batch(self, n: int) -> list[L2Tick]:
        """Return up to ``n`` queued ticks (never blocks)."""
        batch: list[L2Tick] = []
        for _ in range(max(0, int(n))):
            if self._queue.empty():
                break
            item = self._queue.get_nowait()
            if item is None:
                break
            batch.append(item)
        return batch

    async def stop(self) -> None:
        """Stop the driver loop and drain the producer task."""
        self._closed = True
        if self._producer is not None:
            self._producer.cancel()
            try:
                await self._producer
            except asyncio.CancelledError:  # expected: we just cancelled it
                pass
            except Exception:  # transport teardown errors must not propagate
                pass
            self._producer = None

    def close(self) -> None:
        """Request the stream loop to stop after the current message."""
        self._closed = True


__all__ = [
    "FastL2Client",
    "L2Tick",
    "TickStats",
    "DEFAULT_SYMBOLS",
    "BINANCE_WS_BASE",
    "BINANCE_WS_BASE_ALT",
    "main",
    "HAS_ORJSON",
    "HAS_UVLOOP",
    "install_event_loop_policy",
    "parse_message",
    "stream_names",
    "stream_url",
]

# ---------------------------------------------------------------------
# Command-line capture (reproducible live run for T-001)
# ---------------------------------------------------------------------

def main(argv: Sequence[str] | None = None) -> int:
    """Capture raw L2 ticks to Parquet.

    ``python -m src.fast_l2_client --ticks 100000 --out data/l2`` runs the
    T-001 exit criterion (100 000 ticks without a drop) against the live
    feed.  Exit status is non-zero if any tick was dropped or arrived out of
    order, so the run can be used as an unattended acceptance check.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Kepler raw L2 tick capture")
    parser.add_argument("--out", default="data/l2", help="Parquet dataset root")
    parser.add_argument("--ticks", type=int, default=100_000,
                        help="stop after this many ticks (T-001 criterion)")
    parser.add_argument("--seconds", type=float, default=None,
                        help="optional wall-clock cap")
    parser.add_argument("--base", default=BINANCE_WS_BASE,
                        help="WebSocket base URL (see BINANCE_WS_BASE_ALT)")
    parser.add_argument("--symbols", default=",".join(DEFAULT_SYMBOLS))
    parser.add_argument("--levels", type=int, default=DEFAULT_LEVELS)
    parser.add_argument("--rate-ms", type=int, default=DEFAULT_RATE_MS)
    parser.add_argument("--flush-rows", type=int, default=50_000)
    parser.add_argument("--max-reconnects", type=int, default=5,
                        help="give up after this many consecutive transport failures")
    parser.add_argument("--reconnect-delay", type=float, default=1.0)
    args = parser.parse_args(argv)

    from src.tick_buffer import L2ParquetStore, TickBuffer

    symbols = tuple(s.strip().lower() for s in args.symbols.split(",") if s.strip())
    loop_name = install_event_loop_policy()
    client = FastL2Client(symbols, levels=args.levels, rate_ms=args.rate_ms,
                          url=stream_url(symbols, args.levels, args.rate_ms,
                                         base=args.base),
                          max_reconnects=args.max_reconnects,
                          reconnect_delay_s=args.reconnect_delay)
    store = L2ParquetStore(args.out)
    buffer = TickBuffer(store, flush_rows=args.flush_rows)

    print(f"loop={loop_name} orjson={HAS_ORJSON} url={client.url}")

    async def capture() -> int:
        captured = 0
        started = time.time()
        # aclosing(): closing the stream deterministically releases the socket
        # while the loop is still alive (an early `break` alone would leave the
        # async generator for the loop shutdown to finalize).
        async with contextlib.aclosing(client.stream()) as ticks:
            async for tick in ticks:
                buffer.append(tick)
                captured += 1
                if captured % 1000 == 0:
                    rate = captured / max(time.time() - started, 1e-9)
                    print(f"  {captured} ticks, {rate:.1f} ticks/s, "
                          f"invalid_books={client.stats.invalid_books}", flush=True)
                if captured >= args.ticks:
                    break
                if args.seconds is not None and time.time() - started >= args.seconds:
                    break
        buffer.flush()
        return captured

    try:
        captured = asyncio.run(capture())
    except Exception as exc:  # transport gave up: report, never crash silently
        print(f"CAPTURE FAILED after {client.stats.reconnects} reconnect(s): "
              f"{type(exc).__name__}: {exc}")
        print(f"stats={client.stats.as_dict()}")
        return 2

    print(f"captured={captured} stats={client.stats.as_dict()}")
    if client.stats.dropped or client.stats.out_of_order:
        print("ACCEPTANCE FAILED: ticks were dropped or out of order")
        return 1
    print(f"ACCEPTANCE OK: {captured} ticks, dropped=0, out_of_order=0")
    return 0


# Field mapping (docs/DataSpec.md §Normalized Fields): symbol, bids, asks,
# ts_exchange, ts_local, seq are all carried verbatim; ``tick_index`` is the
# tick quantum of docs/TickModel.md.  The ``depth20`` snapshot payload carries
# no exchange timestamp, so ts_exchange_ns is 0 for that stream (recorded in
# docs/DataSpec.md).

if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
