# test_fast_l2_client.py — T-001 raw L2 client tests

"""
Invariant and acceptance tests for ``src/fast_l2_client.py`` (T-001).

Everything here is offline and deterministic (docs/QA_Protocol.md P4):

* the only transport is a loopback ``websockets`` server on 127.0.0.1, or an
  in-process frame source injected through ``connector``;
* the clock is injected, so ``ts_local_ns`` and the Parquet day partition are
  reproducible;
* frames are generated in code — no network, no fixtures on disk.

Checked criteria (docs/TaskQueue.md T-001):

* 100 000 ticks delivered with ``dropped == 0`` and ``out_of_order == 0``;
* raw fidelity: level order and quantities survive decoding verbatim;
* no filtering: malformed/empty books are delivered and counted, never
  dropped (docs/goal.md "no filters", docs/Falsifiability.md F2);
* a transport failure reconnects without losing ticks.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import socket
import sys
from contextlib import asynccontextmanager

import pytest

from src.fast_l2_client import (
    HAS_ORJSON,
    HAS_UVLOOP,
    DEFAULT_SYMBOLS,
    FastL2Client,
    L2Tick,
    parse_message,
    install_event_loop_policy,
    stream_names,
    stream_url,
)

ACCEPTANCE_TICKS = 100_000


# ------------------------------------------------------------------
# Deterministic helpers
# ------------------------------------------------------------------

class FakeClock:
    """Monotonic nanosecond clock: +100 ms per call, fixed epoch."""

    def __init__(self, start: int = 1_700_000_000_000_000_000,
                 step: int = 100_000_000) -> None:
        self.value = start
        self.step = step

    def __call__(self) -> int:
        self.value += self.step
        return self.value


def make_frame(symbol: str, seq: int, mid: float, levels: int = 20) -> str:
    """One depth-N snapshot exactly as docs/DataSpec.md describes it."""
    bids = [[round(mid - 0.5 - i, 4), float(10 + i)] for i in range(levels)]
    asks = [[round(mid + 0.5 + i, 4), float(9 + i)] for i in range(levels)]
    return json.dumps({
        "stream": f"{symbol.lower()}@depth{levels}@100ms",
        "data": {"lastUpdateId": seq, "bids": bids, "asks": asks},
    })


def make_frames(n_per_symbol: int = 1_000, levels: int = 20,
                symbols=DEFAULT_SYMBOLS) -> list[str]:
    """Round-robin frames for all three assets with rising sequence ids."""
    frames: list[str] = []
    for index in range(n_per_symbol):
        for offset, symbol in enumerate(symbols):
            frames.append(make_frame(symbol, seq=1_000_000 + offset + index * len(symbols),
                                     mid=100.0 + offset * 50.0 + index * 1e-4,
                                     levels=levels))
    return frames


class FrameSocket:
    """Minimal socket stand-in: an async iterator over pre-built frames."""

    def __init__(self, frames: list[str]) -> None:
        self.frames = frames
        self.closed = False

    def __aiter__(self) -> "FrameSocket":
        return self

    async def __anext__(self) -> str:
        if self.closed or not self.frames:
            raise StopAsyncIteration
        return self.frames.pop(0)

    async def __aexit__(self, *exc) -> None:  # pragma: no cover - parity
        self.closed = True


def frame_connector(frames: list[str], *, fail_first: bool = False):
    """Build a ``connector`` yielding an in-process frame source."""
    state = {"fail_first": fail_first, "attempts": 0}

    @asynccontextmanager
    async def _connector(url: str, open_timeout: float):
        state["attempts"] += 1
        if fail_first and state["attempts"] == 1:
            raise OSError("simulated transport failure")
        socket_like = FrameSocket(list(frames))
        try:
            yield socket_like
        finally:
            socket_like.closed = True

    _connector.state = state  # type: ignore[attr-defined]
    return _connector


def failing_connector(message: str = "boom"):
    """A transport that never establishes a connection."""

    @asynccontextmanager
    async def _connector(url: str, open_timeout: float):
        raise OSError(message)
        yield  # pragma: no cover - unreachable, keeps the generator shape

    return _connector


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@asynccontextmanager
async def loopback_feed(frames: list[str]):
    """Serve ``frames`` over a real loopback WebSocket (offline)."""
    websockets_server = pytest.importorskip("websockets.asyncio.server")
    port = free_port()

    async def handler(ws) -> None:
        for frame in frames:
            await ws.send(frame)

    async with websockets_server.serve(handler, "127.0.0.1", port) as server:
        yield f"ws://127.0.0.1:{port}"
        server.close()


# ------------------------------------------------------------------
# Pure decoding (no I/O)
# ------------------------------------------------------------------

def test_stream_configuration_matches_dataspec() -> None:
    """DataSpec.md fixes depth20 @ 100 ms for the three mission assets."""
    assert stream_names() == ["btcusdt@depth20@100ms",
                              "ethusdt@depth20@100ms",
                              "solusdt@depth20@100ms"]
    url = stream_url()
    assert url.startswith("wss://")
    assert "btcusdt@depth20@100ms/ethusdt@depth20@100ms/solusdt@depth20@100ms" in url


def test_parse_message_reads_combined_envelope() -> None:
    """symbol / seq / levels are read from the combined-stream envelope."""
    raw = make_frame("btcusdt", seq=42, mid=100.0, levels=3)
    tick = parse_message(raw, ts_local_ns=1_234, tick_index=7)

    assert tick.symbol == "BTCUSDT"
    assert tick.seq == 42
    assert tick.tick_index == 7
    assert tick.ts_local_ns == 1_234
    # depth20 snapshots carry no exchange event time (docs/DataSpec.md).
    assert tick.ts_exchange_ns == 0
    assert len(tick.bids) == 3 and len(tick.asks) == 3
    assert tick.bids[0] == (99.5, 10.0)
    assert tick.is_well_formed()


def test_parse_message_bare_payload_requires_symbol() -> None:
    """A bare payload is accepted only with an explicit symbol."""
    raw = json.dumps({"lastUpdateId": 5,
                      "bids": [["99.0", "1.0"]],
                      "asks": [["101.0", "1.0"]]})
    tick = parse_message(raw, ts_local_ns=1, tick_index=0,
                         default_symbol="ethusdt")
    assert tick.symbol == "ETHUSDT"
    with pytest.raises(ValueError):
        parse_message(raw, ts_local_ns=1, tick_index=0)


def test_parse_message_rejects_non_l2_messages() -> None:
    """Anything that is not an L2 book is an error, not a silently empty tick."""
    with pytest.raises(ValueError):
        parse_message(json.dumps({"result": None, "id": 1}),
                      ts_local_ns=1, tick_index=0)
    with pytest.raises(ValueError):
        parse_message(json.dumps([1, 2, 3]), ts_local_ns=1, tick_index=0)


def test_levels_are_preserved_verbatim() -> None:
    """No sorting, no aggregation, no rounding: raw levels in raw order."""
    # Deliberately ascending bids (invalid per DataSpec) plus a zero quantity.
    raw = json.dumps({"stream": "btcusdt@depth20@100ms",
                      "data": {"lastUpdateId": 9,
                               "bids": [["99.0", "0.0"], ["99.5", "3.0"]],
                               "asks": [["100.5", "2.5"]]}})
    tick = parse_message(raw, ts_local_ns=1, tick_index=0)
    assert tick.bids == ((99.0, 0.0), (99.5, 3.0))
    assert tick.asks == ((100.5, 2.5),)
    assert not tick.is_well_formed()


def test_l2tick_best_bid_ask_on_empty_book() -> None:
    """Empty sides are legal input (self-freeze case) and never raise."""
    tick = L2Tick(symbol="BTCUSDT", bids=(), asks=(), seq=0,
                  ts_exchange_ns=0, ts_local_ns=0, tick_index=0)
    assert tick.best_bid == 0.0 and tick.best_ask == 0.0
    assert not tick.is_well_formed()


def test_accelerators_degrade_gracefully() -> None:
    """ADR-004 is satisfied where applicable (uvloop is POSIX-only)."""
    assert isinstance(HAS_ORJSON, bool) and isinstance(HAS_UVLOOP, bool)
    policy = install_event_loop_policy()
    assert policy in {"uvloop", "asyncio"}
    if sys.platform == "win32":
        # uvloop has no Windows implementation: the stdlib policy must stay.
        assert policy == "asyncio" and not HAS_UVLOOP
    elif HAS_UVLOOP:  # pragma: no cover - platform dependent
        assert policy == "uvloop"


# ------------------------------------------------------------------
# Streaming through the client
# ------------------------------------------------------------------

def test_stream_delivers_ticks_in_order_without_dropping() -> None:
    """In-order delivery, contiguous tick_index, exact counters."""
    frames = make_frames(n_per_symbol=200, levels=20)
    clock = FakeClock()
    client = FastL2Client(url="ws://in-process", clock=clock,
                          connector=frame_connector(frames))

    collected: list[L2Tick] = []

    async def consume(tick: L2Tick) -> None:
        collected.append(tick)

    delivered = asyncio.run(client.run(consume, limit=len(frames)))

    assert delivered == len(frames) == 600
    assert client.stats.received == 600
    assert client.stats.dropped == 0
    assert client.stats.out_of_order == 0
    assert client.stats.invalid_books == 0
    # arrival order is the tick quantum (docs/TickModel.md)
    assert [t.tick_index for t in collected] == list(range(600))
    # symbols cycle btc → eth → sol, exactly as framed
    assert [t.symbol for t in collected[:3]] == ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    # raw fidelity against the generator
    first = json.loads(frames[0])["data"]
    assert collected[0].bids[0] == (float(first["bids"][0][0]),
                                    float(first["bids"][0][1]))
    assert len(collected[0].bids) == 20
    # injected clock: one 100 ms step per tick
    assert collected[1].ts_local_ns - collected[0].ts_local_ns == 100_000_000


def test_empty_and_malformed_books_are_delivered_not_filtered() -> None:
    """Zero-depth and malformed books are counted but never dropped."""
    empty = json.dumps({"stream": "ethusdt@depth20@100ms",
                        "data": {"lastUpdateId": 5, "bids": [], "asks": []}})
    unordered = json.dumps({"stream": "solusdt@depth20@100ms",
                            "data": {"lastUpdateId": 6,
                                     "bids": [["99.0", "1.0"], ["99.5", "2.0"]],
                                     "asks": [["100.0", "1.0"]]}})
    frames = [make_frame("btcusdt", 4, 100.0, 2), empty, unordered]

    client = FastL2Client(url="ws://in-process", clock=FakeClock(),
                          connector=frame_connector(frames))
    collected: list[L2Tick] = []
    delivered = asyncio.run(client.run(collected.append, limit=3))

    assert delivered == 3, "no tick may be dropped, however malformed"
    assert client.stats.dropped == 0
    # btc frame is valid; empty and unordered frames are the two violations
    assert client.stats.invalid_books == 2
    assert collected[1].bids == () and collected[1].asks == ()


def test_sequence_regression_is_counted_but_not_hidden() -> None:
    """A regressing lastUpdateId is recorded (falsifiability), tick kept."""
    frames = [make_frame("btcusdt", 100, 100.0, 2),
              make_frame("btcusdt", 99, 100.0, 2)]
    client = FastL2Client(url="ws://in-process", clock=FakeClock(),
                          connector=frame_connector(frames))
    delivered = asyncio.run(client.run(lambda tick: None, limit=2))

    assert delivered == 2
    assert client.stats.out_of_order == 1
    assert client.stats.dropped == 0


def test_seq_gaps_are_not_drops() -> None:
    """100 ms snapshots jump in lastUpdateId; that is not a missing tick."""
    frames = [make_frame("btcusdt", seq, 100.0, 2)
              for seq in (10, 10_000, 1_000_000)]
    client = FastL2Client(url="ws://in-process", clock=FakeClock(),
                          connector=frame_connector(frames))
    delivered = asyncio.run(client.run(lambda tick: None, limit=3))

    assert delivered == 3
    assert client.stats.out_of_order == 0
    assert client.stats.dropped == 0


def test_transport_failure_reconnects_without_losing_ticks() -> None:
    """One simulated outage: reconnect, resume, no gap in tick_index."""
    frames = make_frames(n_per_symbol=50, levels=5)
    connector = frame_connector(frames, fail_first=True)
    client = FastL2Client(url="ws://in-process", clock=FakeClock(),
                          connector=connector, reconnect_delay_s=0.0,
                          max_reconnects=2)
    collected: list[L2Tick] = []

    delivered = asyncio.run(client.run(collected.append, limit=len(frames)))

    assert delivered == 150
    assert client.stats.reconnects == 1
    assert client.stats.dropped == 0
    assert [t.tick_index for t in collected] == list(range(150))


def test_transport_failure_is_reported_not_hidden() -> None:
    """Giving up must surface the reason (observability), with stats intact."""
    client = FastL2Client(url="ws://in-process", clock=FakeClock(),
                          connector=failing_connector(), reconnect_delay_s=0.0,
                          max_reconnects=1)

    with pytest.raises(OSError):
        asyncio.run(client.run(lambda tick: None, limit=1))

    assert client.stats.reconnects == 1
    assert client.stats.dropped == 0
    assert client.stats.last_error is not None
    assert "OSError" in client.stats.last_error


def test_cli_reports_failure_instead_of_looping_forever(tmp_path) -> None:
    """`python -m src.fast_l2_client` exits 2 when the feed is unreachable."""
    from src.fast_l2_client import main

    closed_port = free_port()   # bound then released: connections are refused
    code = main(["--ticks", "1", "--out", str(tmp_path / "l2"),
                 "--base", f"ws://127.0.0.1:{closed_port}",
                 "--max-reconnects", "0", "--reconnect-delay", "0"])
    assert code == 2


def test_driver_queue_blocks_instead_of_dropping() -> None:
    """pop_batch mode with a tiny queue loses nothing (back-pressure)."""
    frames = make_frames(n_per_symbol=100, levels=2)
    client = FastL2Client(url="ws://in-process", clock=FakeClock(),
                          connector=frame_connector(frames), queue_size=4)

    async def driver() -> int:
        await client.start()
        received = 0
        try:
            for _ in range(2_000):
                batch = await client.pop_batch(16)
                received += len(batch)
                if received >= len(frames):
                    break
                await asyncio.sleep(0)
        finally:
            await client.stop()
        return received

    received = asyncio.run(asyncio.wait_for(driver(), timeout=30))
    assert received == len(frames) == 300
    assert client.stats.dropped == 0
    assert client.stats.received == 300


# ------------------------------------------------------------------
# Acceptance: 100 000 ticks without a drop (roadmap Phase 1 exit criterion)
# ------------------------------------------------------------------

def test_acceptance_100k_ticks_without_drop() -> None:
    """T-001 exit criterion: 100 000 ticks, dropped == 0, out_of_order == 0."""
    symbols = DEFAULT_SYMBOLS
    mid = {"BTCUSDT": 100.0, "ETHUSDT": 200.0, "SOLUSDT": 50.0}
    counters = {symbol: 1_000_000 for symbol in symbols}

    def frame_for(index: int) -> str:
        symbol = symbols[index % len(symbols)]
        counters[symbol] += 1
        return make_frame(symbol, counters[symbol],
                          mid[symbol.upper()] + index * 1e-6, levels=5)

    frames = [frame_for(i) for i in range(ACCEPTANCE_TICKS)]
    client = FastL2Client(url="ws://in-process", clock=FakeClock(),
                          connector=frame_connector(frames))

    counts: dict[str, int] = {s.upper(): 0 for s in symbols}
    last_index = -1

    def consume(tick: L2Tick) -> None:
        nonlocal last_index
        counts[tick.symbol] += 1
        last_index = tick.tick_index

    delivered = asyncio.run(client.run(consume, limit=ACCEPTANCE_TICKS))

    assert delivered == ACCEPTANCE_TICKS
    assert client.stats.received == ACCEPTANCE_TICKS
    assert client.stats.dropped == 0
    assert client.stats.out_of_order == 0
    assert client.stats.invalid_books == 0
    assert last_index == ACCEPTANCE_TICKS - 1
    # round-robin framing: the remainder goes to the first assets
    expected_counts = {
        symbol.upper(): ACCEPTANCE_TICKS // len(symbols)
        + (1 if offset < ACCEPTANCE_TICKS % len(symbols) else 0)
        for offset, symbol in enumerate(symbols)
    }
    assert counts == expected_counts


# ------------------------------------------------------------------
# Real loopback WebSocket (same client code path, real transport)
# ------------------------------------------------------------------

def test_loopback_websocket_stream_is_ordered_and_complete() -> None:
    """End-to-end over 127.0.0.1: identical guarantees, real transport."""
    frames = make_frames(n_per_symbol=400, levels=20)

    async def scenario() -> tuple[int, list[L2Tick], object]:
        async with loopback_feed(frames) as url:
            client = FastL2Client(url=url, clock=FakeClock())
            collected: list[L2Tick] = []
            delivered = await client.run(collected.append, limit=len(frames))
            return delivered, collected, client.stats

    delivered, collected, stats = asyncio.run(asyncio.wait_for(scenario(), timeout=60))

    assert delivered == len(frames) == 1_200
    assert stats.dropped == 0
    assert stats.out_of_order == 0
    assert stats.invalid_books == 0
    assert [t.tick_index for t in collected] == list(range(1_200))
    assert [t.symbol for t in collected[:3]] == ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    sent = json.loads(frames[3])["data"]
    assert collected[3].asks[0] == (float(sent["asks"][0][0]),
                                    float(sent["asks"][0][1]))
