# Changelog

## v0.6.0 — 2026-10-07 (Session 2: audit, doc reorg, virial resolution)
- Audit: measured 7/9 tests at session start (brief claimed 8/9); unreported
  I2 float32 failure found; three inherited claims corrected (ResearchLog).
- `docs/` reorganized into 12 numbered categories; new `00_INDEX.md`,
  `STATE_INVENTORY.md`, `06_research/` registry (R-PHY-001..004,
  R-DET-001/002, R-MM-001); `generate_docs.py` retargeted to the nested tree.
- `src/physics_jax.py`: isotropic (radial) ε-softening for multi-D states in
  `compute_potential_energy` / `acceleration` / `compute_self_induced_G`;
  shape-safe `acceleration`; consistent `max|I|` initial imbalance statistic.
  1-D numerics unchanged (bit-identical).
- `tests/test_physics.py`: `test_virial_ratio_convergence` rebuilt on a 2-D
  circular orbit with exact v_circ derivation; per-tick AND averaged I4 check;
  former −1.0 root-caused as assignment bug + radial-plunge heating (F10);
  thresholds untouched. Test header documents float64 requirement.
- `tests/conftest.py`: enable JAX float64 (precision for 1e−9 class bounds).
- `src/__init__.py`: package marker.
- Docs: FailureModes +F10 (F8 clarified); Conflicts CON-002 RESOLVED,
  CON-003 OPEN (G fallback magic 1.0; frozen-vs-running G); Hypotheses H2
  revised; Invariants I2/I4 scoped; Physics.md numerical-requirements section;
  TaskQueue T-003/T-004 completed, T-008/T-009 added.
- Status: **9/9 tests pass.**

## v0.1.0 — 2025-01
- Initial Concept, Philosophy, Strategy.

## v0.2.0 — 2025-01
- Added Implementation.
- Introduced physics_jax.

## v0.3.0 — 2025-01
- Added detectors_numba.
- Added market_maker (A-S).

## v0.4.0 — 2025-01
- Migrated to uvloop + orjson.
- Added fast_l2_client.

## v0.5.0 — 2025-01
- Ten L2 states.
- simulation_live_v3.

## v1.0.0 — (target)
- 10 million ticks.
- Full validation.
- Whitepaper.

## [2026-10-07] — physics_jax.py
- Implemented `symplectic_step` (velocity Verlet)
- Implemented `integrate` with lax.scan
- JAX pytree registration for ThreeBodyState
- Invariant tests: energy, angular momentum, virial, imbalance
- Zero-mass (empty book) support without NaN

## [2026-10-07] — Documentation Migration
- Translated all Persian/Korean documentation to English
- Rejected ADR-007 (G_DEFAULT violates Axiom 4)
- Added self-induced gravity formula to Physics.md
- Created coordination files (AgentSync, AgentHandoff, QA_Protocol, etc.)
