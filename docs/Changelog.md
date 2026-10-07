# Changelog

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
