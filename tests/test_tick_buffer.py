# test_tick_buffer.py — T-002 tick buffer, Parquet storage and replay tests

"""
Tests for ``src/tick_buffer.py`` (T-002).

All offline and deterministic (docs/QA_Protocol.md P4): ticks are synthesised
in code and written to pytest's ``tmp_path``.

Checked criteria (docs/TaskQueue.md T-002, docs/DataSpec.md):

* every field and every level survives the Parquet round trip unchanged;
* storage is partitioned ``symbol=<S>/day=<YYYY-MM-DD>`` with zstd
  compression;
* ``tick_index`` ordering is enforced, not repaired;
* replay is deterministic and can feed ``state_from_l2`` and ``integrate``;
* an empty dataset replays to nothing instead of raising.
"""

from __future__ import annotations

import datetime as dt
import itertools
from pathlib import Path

import jax.numpy as jnp
import pytest

from src.fast_l2_client import L2Tick
from src.physics_jax import integrate, state_from_l2
from src.tick_buffer import (
    L2ParquetStore,
    TickBuffer,
    TickOrderError,
    TickReplay,
    parquet_codecs,
    replay_summary,
    row_to_tick,
    tick_to_row,
)

SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT")
DAY_A = "2026-10-10"
DAY_B = "2026-10-11"


def day_ns(day: str, hour: int = 12) -> int:
    date = dt.datetime.strptime(day, "%Y-%m-%d").replace(
        hour=hour, tzinfo=dt.timezone.utc)
    return int(date.timestamp()) * 1_000_000_000


def make_tick(symbol: str, index: int, *, mid: float,
              levels: int = 5, day: str = DAY_A,
              ts_exchange_ns: int = 0, seq: int | None = None) -> L2Tick:
    """A well-formed raw tick: bids descending, asks ascending, depth > 0."""
    bids = tuple((round(mid - 0.5 - i, 6), float(1 + i)) for i in range(levels))
    asks = tuple((round(mid + 0.5 + i, 6), float(2 + i)) for i in range(levels))
    return L2Tick(
        symbol=symbol,
        bids=bids,
        asks=asks,
        seq=seq if seq is not None else 1_000 + index,
        ts_exchange_ns=ts_exchange_ns,
        ts_local_ns=day_ns(day) + index * 100_000_000,
        tick_index=index,
    )


def dataset(tmp_path: Path, *, n_per_symbol: int = 40,
            levels: int = 5) -> tuple[L2ParquetStore, list[L2Tick]]:
    """Round-robin three-asset dataset written through a TickBuffer."""
    store = L2ParquetStore(tmp_path / "l2")
    buffer = TickBuffer(store, flush_rows=1_000)
    ticks: list[L2Tick] = []
    index = 0
    for step in range(n_per_symbol):
        for offset, symbol in enumerate(SYMBOLS):
            tick = make_tick(symbol, index, mid=100.0 + 50.0 * offset + step * 1e-3,
                             levels=levels)
            ticks.append(tick)
            buffer.append(tick)
            index += 1
    buffer.flush()
    return store, ticks


# ------------------------------------------------------------------
# Storage: fidelity, layout, compression
# ------------------------------------------------------------------

def test_row_round_trip_is_exact() -> None:
    """row_to_tick(tick_to_row(t)) == t, including empty sides."""
    ticks = [make_tick("BTCUSDT", 0, mid=101.25, levels=20),
             make_tick("SOLUSDT", 1, mid=50.5, levels=1)]
    for tick in ticks:
        assert row_to_tick(tick_to_row(tick)) == tick

    empty = L2Tick(symbol="SOLUSDT", bids=(), asks=(), seq=0,
                   ts_exchange_ns=0, ts_local_ns=day_ns(DAY_A), tick_index=2)
    assert row_to_tick(tick_to_row(empty)) == empty


def test_every_field_survives_parquet(tmp_path: Path) -> None:
    """Full round trip through Parquet preserves all fields and level order."""
    store, ticks = dataset(tmp_path, n_per_symbol=7, levels=20)
    restored = list(store.read_rows())

    assert len(restored) == len(ticks)
    by_index = {tick.tick_index: tick for tick in ticks}
    for row in restored:
        original = by_index[row["tick_index"]]
        assert row_to_tick(row) == original
        assert len(row["bid_prices"]) == 20
        assert row["bid_prices"] == [p for p, _ in original.bids]
        assert row["bid_quantities"] == [q for _, q in original.bids]
        assert row["ask_prices"] == [p for p, _ in original.asks]
        assert row["ask_quantities"] == [q for _, q in original.asks]


def test_partition_layout_and_zstd_compression(tmp_path: Path) -> None:
    """docs/DataSpec.md §Storage: symbol/day partitions, Parquet, zstd."""
    store = L2ParquetStore(tmp_path / "l2")
    store.write([make_tick("BTCUSDT", 0, mid=100.0, day=DAY_A),
                 make_tick("ETHUSDT", 1, mid=200.0, day=DAY_A),
                 make_tick("BTCUSDT", 2, mid=100.0, day=DAY_B)])

    relative = sorted(
        f"{path.parent.parent.name}/{path.parent.name}/{path.name}"
        for path in store.files()
    )
    assert relative == [
        f"symbol=BTCUSDT/day={DAY_A}/part-0001.parquet",
        f"symbol=BTCUSDT/day={DAY_B}/part-0001.parquet",
        f"symbol=ETHUSDT/day={DAY_A}/part-0001.parquet",
    ]
    for path in store.files():
        assert set(parquet_codecs(path)) == {"ZSTD"}, \
            "Parquet must use zstd (DataSpec.md §Storage)"


def test_footer_reader_actually_discriminates_codecs(tmp_path: Path) -> None:
    """The zstd assertion has teeth: the reader reports other codecs too."""
    store = L2ParquetStore(tmp_path / "zstd")
    store.write([make_tick("BTCUSDT", 0, mid=100.0)])

    plain = L2ParquetStore(tmp_path / "plain", compression="uncompressed")
    plain.write([make_tick("BTCUSDT", 0, mid=100.0)])

    assert set(parquet_codecs(store.files()[0])) == {"ZSTD"}
    assert set(parquet_codecs(plain.files()[0])) == {"UNCOMPRESSED"}
    assert store.files()[0] != plain.files()[0]


def test_reopening_a_store_appends_without_overwriting(tmp_path: Path) -> None:
    """A second writer session continues the part numbering."""
    root = tmp_path / "l2"
    L2ParquetStore(root).write([make_tick("BTCUSDT", 0, mid=100.0)])
    store = L2ParquetStore(root)
    store.write([make_tick("BTCUSDT", 1, mid=100.0)])

    names = sorted(path.name for path in store.files())
    assert names == ["part-0001.parquet", "part-0002.parquet"]
    assert len(list(store.read_rows())) == 2


# ------------------------------------------------------------------
# Buffer: ordering guarantee and bounded memory
# ------------------------------------------------------------------

def test_buffer_rejects_out_of_order_ticks(tmp_path: Path) -> None:
    """Ordering is enforced, never silently repaired."""
    buffer = TickBuffer(L2ParquetStore(tmp_path / "l2"), flush_rows=100)
    buffer.append(make_tick("BTCUSDT", 5, mid=100.0))

    with pytest.raises(TickOrderError):
        buffer.append(make_tick("BTCUSDT", 5, mid=100.0))
    with pytest.raises(TickOrderError):
        buffer.append(make_tick("BTCUSDT", 4, mid=100.0))

    buffer.append(make_tick("BTCUSDT", 6, mid=100.0))
    assert buffer.pending == 2


def test_buffer_auto_flushes_and_bounds_memory(tmp_path: Path) -> None:
    """The in-memory block never exceeds flush_rows (no unbounded memory)."""
    store = L2ParquetStore(tmp_path / "l2")
    buffer = TickBuffer(store, flush_rows=3)
    written: list[Path] = []

    for index in range(7):
        written.extend(buffer.append(make_tick("BTCUSDT", index, mid=100.0)))
        assert buffer.pending <= 2

    assert len(written) == 2            # after 3 and after 6 appends
    assert buffer.pending == 1
    buffer.flush()
    assert buffer.pending == 0
    assert len(list(store.read_rows())) == 7
    assert buffer.stats.written == 7


# ------------------------------------------------------------------
# Replay: determinism, alignment, physics hand-off
# ------------------------------------------------------------------

def test_replay_is_deterministic(tmp_path: Path) -> None:
    """Two replays of the same dataset return the identical sequence."""
    store, ticks = dataset(tmp_path, n_per_symbol=25)
    replay = TickReplay(store.root)

    first = list(replay.ticks())
    second = list(replay.ticks())
    assert first == second
    assert [tick.tick_index for tick in first] == [tick.tick_index for tick in ticks]
    assert first == ticks


def test_replay_emits_one_state_per_tick_after_warmup(tmp_path: Path) -> None:
    """Latest-wins alignment: states start once all three assets have a book."""
    _, ticks = dataset(tmp_path, n_per_symbol=20)
    replay = TickReplay(tmp_path / "l2")

    states = list(replay.states())
    # the first two ticks cannot form a three-body state
    assert len(states) == len(ticks) - (len(SYMBOLS) - 1)

    latest: dict[str, L2Tick] = {}
    for tick in ticks:
        latest[tick.symbol] = tick
    expected = state_from_l2(*[
        jnp.asarray(levels, dtype=jnp.float64)
        for symbol in SYMBOLS
        for levels in (latest[symbol].bids, latest[symbol].asks)
    ])
    assert jnp.allclose(states[-1].x, expected.x)
    assert jnp.allclose(states[-1].m, expected.m)
    assert jnp.allclose(states[-1].I, expected.I)


def test_replayed_states_feed_the_integrate_loop(tmp_path: Path) -> None:
    """Replay → state_from_l2 → integrate: deterministic, invariants hold."""
    _, ticks = dataset(tmp_path, n_per_symbol=30)
    replay = TickReplay(tmp_path / "l2")

    state_0 = next(iter(replay.states()))
    L_norm, energy, potential, imbalance = integrate(state_0, 500)

    # No NaN/Inf may enter the integrator from stored data (F1 self-freeze).
    assert jnp.all(jnp.isfinite(L_norm))
    assert jnp.all(jnp.isfinite(energy))
    assert jnp.all(jnp.isfinite(potential))
    assert jnp.all(jnp.isfinite(state_0.m)) and jnp.all(state_0.m >= 0.0)
    assert float(jnp.max(imbalance)) <= 1.0 + 1e-12      # I6

    # same state, same ticks ⇒ same trajectory (reproducible replay)
    again = next(iter(TickReplay(tmp_path / "l2").states()))
    L_again, *_ = integrate(again, 500)
    assert jnp.allclose(L_norm, L_again, atol=1e-15)


def test_replay_filters_by_symbol_and_day(tmp_path: Path) -> None:
    """Filters select partitions and keep replay deterministic."""
    store = L2ParquetStore(tmp_path / "l2")
    ticks = []
    index = 0
    for day in (DAY_A, DAY_B):
        for symbol in SYMBOLS:
            ticks.append(make_tick(symbol, index, mid=100.0, day=day))
            index += 1
    store.write(ticks)

    day_a_ticks = list(TickReplay(store, days=[DAY_A]).ticks())
    assert {tick.symbol for tick in day_a_ticks} == set(SYMBOLS)
    assert all(tick.ts_local_ns < day_ns(DAY_B, hour=0) for tick in day_a_ticks)
    assert [tick.tick_index for tick in day_a_ticks] == sorted(
        tick.tick_index for tick in day_a_ticks)

    only_eth = list(TickReplay(store, symbols=["ETHUSDT"]).ticks())
    assert {tick.symbol for tick in only_eth} == {"ETHUSDT"}
    assert len(only_eth) == 2


def test_empty_dataset_replays_to_nothing(tmp_path: Path) -> None:
    """No data is not an error: replay is simply empty."""
    store = L2ParquetStore(tmp_path / "l2")
    replay = TickReplay(store.root)

    assert list(replay.ticks()) == []
    assert list(replay.states()) == []
    assert replay_summary(store)["total"] == 0


def test_replay_summary_counts_and_range(tmp_path: Path) -> None:
    """Audit counters expose coverage without loading JAX."""
    store, ticks = dataset(tmp_path, n_per_symbol=15)
    summary = replay_summary(store)

    assert summary["total"] == len(ticks)
    assert summary["per_symbol"] == {symbol: 15 for symbol in SYMBOLS}
    assert summary["first_tick_index"] == 0
    assert summary["last_tick_index"] == len(ticks) - 1


# ------------------------------------------------------------------
# Real data: the committed live capture (tests/data/live_2026-10-11)
#
# These assertions cover the *retention* guarantees only. The physics
# invariants do NOT hold on this data at dt = 1 tick (CON-008, F10), and that
# failure must not be turned into a passing test.
# ------------------------------------------------------------------

LIVE_FIXTURE = Path(__file__).parent / "data" / "live_2026-10-11"


def test_committed_live_capture_replays_with_all_guarantees() -> None:
    """Real Binance snapshots survive storage and replay intact."""
    store = L2ParquetStore(LIVE_FIXTURE)
    assert store.files(), "fixture missing: tests/data/live_2026-10-11"
    assert {codec for path in store.files() for codec in parquet_codecs(path)} == {"ZSTD"}

    ticks = list(TickReplay(LIVE_FIXTURE).ticks())
    assert len(ticks) == 2_785
    assert {tick.symbol for tick in ticks} == set(SYMBOLS)
    # arrival order is preserved exactly (tick quantum, docs/TickModel.md)
    assert [tick.tick_index for tick in ticks] == list(range(len(ticks)))
    assert all(a.ts_local_ns <= b.ts_local_ns for a, b in zip(ticks, ticks[1:]))
    # every real snapshot is a well-formed 20-level book (I7 at ingestion)
    assert all(tick.is_well_formed() for tick in ticks)
    assert all(len(tick.bids) == 20 and len(tick.asks) == 20 for tick in ticks)
    assert all(float(q) > 0 for tick in ticks for _, q in tick.bids + tick.asks)

    summary = replay_summary(store)
    assert summary["total"] == 2_785
    assert summary["per_symbol"] == {"BTCUSDT": 1_165, "ETHUSDT": 1_151,
                                    "SOLUSDT": 469}


def test_committed_live_capture_replay_is_deterministic() -> None:
    """Same dataset ⇒ same tick sequence and same three-body states."""
    first = list(TickReplay(LIVE_FIXTURE).ticks())
    second = list(TickReplay(LIVE_FIXTURE).ticks())
    assert first == second

    # latest-wins alignment: the first two ticks cannot span three bodies
    assert len({first[0].symbol, first[1].symbol}) == 2

    # Determinism is checked on a prefix only: state_from_l2 costs ~13 ms per
    # tick (measured), so materialising all 2 783 states would dominate the
    # suite runtime without adding evidence.
    states_a = list(itertools.islice(TickReplay(LIVE_FIXTURE).states(), 200))
    states_b = list(itertools.islice(TickReplay(LIVE_FIXTURE).states(), 200))
    assert len(states_a) == len(states_b) == 200
    for s_a, s_b in zip(states_a, states_b):
        assert jnp.array_equal(s_a.x, s_b.x)
        assert jnp.array_equal(s_a.m, s_b.m)
        assert jnp.array_equal(s_a.I, s_b.I)
    # masses come from real depths: finite and non-negative
    assert jnp.all(jnp.isfinite(states_a[0].m))
    assert jnp.all(states_a[0].m >= 0.0)
    assert jnp.all(jnp.isfinite(states_a[0].I))
