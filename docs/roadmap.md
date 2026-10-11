# Roadmap

> **Immutable Principle:** No risk management, no filters, no indicators, no external parameters.

## Phase 0: Theoretical Foundation ✅
- Philosophy, Concept, Strategy, Implementation, Notation, Glossary

## Phase 1: Tick Infrastructure
- DataSpec, TickModel, fast_l2_client, tick_buffer, replay
- Exit criteria: 100,000 ticks without drop
- Status (2026-10-11): **code complete and verified offline.**
  `src/fast_l2_client.py` (raw `depth20@100ms` snapshots) and
  `src/tick_buffer.py` (Parquet/zstd store + deterministic replay) exist with
  tests; the 100,000-tick acceptance run passes with `dropped == 0` and
  `out_of_order == 0` against an injected/in-process source and a loopback
  WebSocket. A live public-feed run has **not** been performed (the sandbox
  used for verification is offline), so the exit criterion is verified
  offline only.

## Phase 2: Physics
- Physics, physics_jax, Invariants
- Exit criteria: ‖L‖ bounded 90% of time

## Phase 3: Detectors
- Detectors, detectors_numba, K-S test
- Exit criteria: F1 > 0.8

## Phase 4: Market Making
- MarketMaking, market_maker
- Exit criteria: spread always positive

## Phase 5: Simulation
- 10 million ticks
- Exit criteria: Π > 0 with 95% CI

## Phase 6: Validation
- Hypotheses, Experiments, t-test, bootstrap
- Exit criteria: reject/confirm main hypothesis

## Phase 7: Mathematical Extension
- Differential geometry, Ricci, gauge, quantization

## Phase 8: Multidimensional
- JAX vmap on 3 time-frames

## Phase 9: Final Documentation
- References, OpenProblems, whitepaper

## Phase 10: Unified Theory
- Orbit ↔ Profit ↔ Information

## Timeline
| Phase | Duration |
|-------|----------|
| 0 | ✅ |
| 1 | 2 weeks |
| 2 | 3 weeks |
| 3 | 2 weeks |
| 4 | 2 weeks |
| 5 | 4 weeks |
| 6 | 2 weeks |
| 7 | 6 weeks |
| 8 | 3 weeks |
| 9 | 2 weeks |
