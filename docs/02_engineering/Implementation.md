# Implementation Status and Architecture

## 1. Implemented data/physics path

```text
raw L2 WebSocket snapshots
  → FastL2Client
  → bounded TickBuffer
  → Parquet/zstd store
  → deterministic TickReplay
  → state_from_l2
  → physics_jax
```

The ingestion, buffer/store/replay, and physics modules exist. This describes code paths, not proof that the three-body model is valid on real data; see CON-008/F10. Planned modules are listed in §6.

## 2. Technology status

| Layer | Library | Status |
|---|---|---|
| Async event loop | `asyncio`; optional `uvloop` | Used where available; stdlib fallback (ADR-010) |
| WebSocket | `websockets` | Used by `src/fast_l2_client.py` (T-001) |
| JSON | `orjson`; stdlib fallback | Optional acceleration (ADR-010) |
| Physics | JAX, float64 | Used by `src/physics_jax.py`; synthetic tests pass in the recorded environment; real-data I1/I2 conflict remains open |
| Detectors | Numba (planned) | Reserved by ADR-003; no detector module is implemented |
| Storage | Polars / Parquet + zstd | Used by `src/tick_buffer.py` (T-002); some CPUs require the compatible runtime extra (ADR-011) |

## 3. Repository layout

```text
Kepler/
├── AGENTS.md
├── docs/
│   ├── 01_theory/
│   ├── 02_engineering/
│   ├── 03_research/
│   ├── 04_planning/
│   └── 05_reference/
├── src/
│   ├── fast_l2_client.py
│   ├── tick_buffer.py
│   └── physics_jax.py
├── tests/
│   ├── test_fast_l2_client.py
│   ├── test_tick_buffer.py
│   ├── test_physics.py
│   └── data/live_2026-10-11/
└── requirements.txt
```

The docs index lists all canonical documents. Flat `docs/<name>.md` files are compatibility stubs. The implemented Python modules remain flat until a measured need justifies a package split.

## 4. Data flow and invariants

- The client decodes and retains the snapshot fields; book validation is counted, not used to silently filter a tick.
- The buffer is bounded and flushes to the partitioned Parquet store.
- Replay is deterministic and constructs model state from the latest available snapshots according to ADR-011.
- Raw ticks are stored; model-derived values are recomputed at replay time.
- A synthetic physics test is not a real-data validation. Report the CON-008 failure with any real-data result.

## 5. Engineering constraints

Avoid unbounded memory and silent tick filtering. Avoid adding dependencies without a measured need and an ADR where appropriate. Do not add quote output or exchange connectivity for order placement.

## 6. Planned, not implemented

```text
replayed ticks → research detectors → [scope decision required] → simulation/validation
```

`detectors_numba`, market-making/quote generation, long-run simulation, and validation modules are not present. In particular, do not infer an exchange-execution layer from the old pipeline diagrams or strategy sketches.

## 7. Verification

Use the tests under `tests/`. The last recorded pinned-environment run reported 41 passing tests; run the suite in the current environment before claiming current verification. Live-feed captures are optional research measurements, not a substitute for deterministic tests, and must be reported separately.
