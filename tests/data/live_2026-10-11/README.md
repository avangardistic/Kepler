# Live L2 capture — 2026-10-11

Raw Binance `depth20@100ms` snapshots for the three mission assets, captured
with the Phase 1 client. Committed so the CON-008 experiment (real-data
invariant failure) and the storage/replay guarantees can be reproduced without
a network connection.

## How it was produced

```bash
python -m src.fast_l2_client \
    --base wss://data-stream.binance.vision/stream \
    --ticks 3000 --seconds 120 --out tests/data/live_2026-10-11
```

* `stream.binance.com` answered **HTTP 451** from the capture network; the
  `.vision` market-data domain served the identical payloads (CON-007).
* Nothing was filtered, aggregated or repaired: these are the raw snapshots as
  the exchange sent them (20 levels per side on every tick).

## Contents

| Symbol | Ticks |
|---|---|
| BTCUSDT | 1 165 |
| ETHUSDT | 1 151 |
| SOLUSDT | 469 |
| **total** | **2 785** |

* Ticks (up to the 120 s cap), `dropped = 0`, `out_of_order = 0`,
  `invalid_books = 0`, `reconnects = 0`.
* Parquet + zstd, partitioned `symbol=<S>/day=2026-10-11/part-0001.parquet`
  (verified with `src.tick_buffer.parquet_codecs`, which needs no extra
  dependency).
* Size: 72 KB (26.6 bytes/tick).

## Why it is committed

`docs/FailureModes.md` F10 and `docs/Conflicts.md` CON-008 record that I1/I2
fail when this data is replayed at `dt = 1` tick:

| Path (2 000 ticks, dt = 1) | ‖L‖₀ | ‖L‖ₘₐₓ | E₀ | max relative energy drift |
|---|---|---|---|---|
| 2-D `state_from_l2`, conservative | 0 | 0 | −1.008 | 281 |
| 2-D `state_from_l2`, with imbalance + friction | 0 | 6.25e4 | −1.008 | 6.2e6 |
| 1-D ⇒ ADR-008 embedding, conservative | 8.484 | 8.484 | −0.6255 | 1.54 |
| 1-D ⇒ ADR-008 embedding, with imbalance + friction | 8.484 | 1.65e6 | −0.6255 | 1e7 |

Tests over this fixture assert only the **retention** guarantees (all fields,
level order, 20 levels, ordering, valid books, zstd codec, deterministic
replay) — never that the physics invariants hold, because on this data they do
not. Do not convert that failure into a passing assertion.

## Reproducing the measurement

```python
from src.tick_buffer import TickReplay
from src.physics_jax import integrate

state = next(iter(TickReplay("tests/data/live_2026-10-11").states()))
L_norm, energy, potential, imbalance = integrate(state, 2000, dt=1.0)
```

Note: `tests/data/**` is a frozen record. Never rewrite it in place; capture a
new directory instead.
