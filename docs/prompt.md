# Task Queue

## Status: Active

> **Sync note (2026-10-10).** T-003 and T-004 were completed in code and tests
> but had never been moved out of "Open". They are now recorded under
> "Completed" with their verification evidence. No code was changed by this
> sync; `pytest tests/ -v` still reports 9 passed.

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

### T-005 [Phase 3] [High]
- **Title:** detectors_numba.py
- **Input:** Detectors.md
- **Output:** Iceberg + Spoof
- **Criterion:** F1 > 0.8 on synthetic data
- **Blocked by:** T-001, T-002 (needs recorded L2 ticks)

### T-006 [Phase 4] [High]
- **Title:** market_maker.py
- **Input:** MarketMaking.md
- **Output:** quote_all
- **Criterion:** bid < ask always
- **Blocked by:** T-001, T-002 (needs recorded L2 ticks)

### T-007 [Phase 5] [High]
- **Title:** simulation_live_v3
- **Input:** All
- **Output:** 10M tick simulation
- **Criterion:** Pi > 0 with 95% CI
- **Blocked by:** T-001 … T-006

## In Progress
(Empty)

## Completed
- [x] T-000 [Phase 0] Generate all docs
- [x] T-003 [Phase 2] physics_jax.py — `src/physics_jax.py` implements
      `symplectic_step` (velocity Verlet) and `integrate` (`lax.scan`).
      Verified 2026-10-10 with jax 0.10.2 / pytest 9.1.1 on Python 3.11:
      `pytest tests/ -v` → 9 passed.
      Criterion re-checked: I1 angular momentum bounded, I2 relative energy
      drift < 1e-9 (requires the x64 flag set in code per ADR-002).
- [x] T-004 [Phase 2] Invariant tests — `tests/test_physics.py` (9 tests):
      angular momentum (zero at rest, bounded over 10k ticks, cumulative
      series recorded), energy conservation, virial ratio (I4), imbalance
      bound (I6), zero-depth freeze, ε-softening, determinism.
      All pass in the default configuration.

## Prioritization
1. T-001, T-002 (infrastructure) — everything downstream needs recorded L2 ticks.
2. T-005 (detection)
3. T-006 (MM)
4. T-007 (integration)

## Known follow-ups (not tasks yet)
- Running time-average of ⟨d²⟩ for the self-induced coupling: `integrate`
  currently fixes `G` from the initial state (see Conflicts.md CON-005,
  open remark). Needs a decision before Phase 5.
- Measure the residual of the rigid-rotation embedding for N ≥ 3 (ADR-008):
  exact only for two bodies.
- `docs/Changelog.md` entries v0.2.0–v0.5.0 describe modules that are not in
  the repository; they are planned, not delivered. See roadmap.md.
