# Task Queue

## Status: Active

## Open

### T-001 [Phase 1] [High]
- **Title:** Implement fast_l2_client.py
- **Input:** DataSpec.md
- **Output:** WebSocket client
- **Criterion:** Receive 10,000 ticks without dropout

### T-002 [Phase 1] [High]
- **Title:** tick_buffer with polars
- **Input:** DataSpec.md
- **Output:** Parquet storage
- **Criterion:** Deterministic retrieval

### T-003 [Phase 2] [High]
- **Title:** physics_jax.py
- **Input:** Physics.md
- **Output:** symplectic_step
- **Criterion:** Angular momentum conservation to 1e-9

### T-004 [Phase 2] [Medium]
- **Title:** Invariant tests
- **Input:** Invariants.md
- **Output:** tests/test_physics.py
- **Criterion:** All pass

### T-005 [Phase 3] [High]
- **Title:** detectors_numba.py
- **Input:** Detectors.md
- **Output:** Iceberg + Spoof
- **Criterion:** F1 > 0.8 on synthetic data

### T-006 [Phase 4] [High]
- **Title:** market_maker.py
- **Input:** MarketMaking.md
- **Output:** quote_all
- **Criterion:** bid < ask always

### T-007 [Phase 5] [High]
- **Title:** simulation_live_v3
- **Input:** All
- **Output:** 10M tick simulation
- **Criterion:** Pi > 0 with 95% CI

## In Progress
(Empty)

## Completed
- [x] T-000 [Phase 0] Generate all docs

## Prioritization
1. T-001, T-002 (infrastructure)
2. T-003, T-004 (physics)
3. T-005 (detection)
4. T-006 (MM)
5. T-007 (integration)
