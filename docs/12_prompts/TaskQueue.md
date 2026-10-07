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

### New (Session 2, 2026-10-07)

### T-008 [Phase 2] [High]
- **Title:** Generalized virial identity test (I≠0, γ≠0)
- **Input:** `06_research/physics/generalized_virial.md` (derivation done)
- **Output:** `tests/test_physics.py::test_generalized_virial_identity`
- **Criterion:** |2⟨T⟩+⟨V⟩+⟨Σ mᵢIᵢxᵢ⟩−⟨Σ γᵢ|vᵢ|²⟩| / |⟨V⟩| < 0.2 over exact
  integer periods, config passes R-PHY-003 preflight. Failure → F9 falsification.

### T-009 [Phase 2] [Medium]
- **Title:** Collision-resolution preflight + dt/eccentricity sweep (R-PHY-003)
- **Input:** `06_research/physics/orbital_conditions.md`
- **Output:** shared test helper + sweep table
- **Criterion:** helper rejects the historical F10 configs; sweep boundary
  documented.

### T-010 [Phase 2] [Blocking decision]
- **Title:** CON-003 adjudication (G fallback; frozen-vs-running G) — HUMAN/ADR
- **Input:** `06_research/physics/gravity_derivation.md`, `08_failures/Conflicts.md`
- **Output:** ADR-008 + Physics.md alignment (+ engine change if decided)

## In Progress
(Empty)

## Completed
- [x] T-000 [Phase 0] Generate all docs
- [x] T-003 [Phase 2] physics_jax.py + symplectic_step — L conserved to 1e−14
      in float64 (criterion 1e−9 met; Session 2, multi-D softening fix included)
- [x] T-004 [Phase 2] Invariant tests — 9/9 pass; CON-002 resolved;
      F10 documented (Session 2, 2026-10-07)

## Prioritization
1. T-010 (decision — unblocks honest generalization of H2/I2), then T-008, T-009 (physics research)
2. T-001, T-002 (infrastructure)
3. T-005 (detection; gated by R-DET-001/002 formalization)
4. T-006 (MM; gated by R-MM-001 audit)
5. T-007 (integration)
Completed: T-003, T-004 (physics core) — 9/9 tests.
