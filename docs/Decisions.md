# Decisions (ADR)

## ADR-001: Microprice Selection Over Mid
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Microprice is sensitive to order flow imbalance.
**Rejected alternative:** mid (blind to volume).

## ADR-002: JAX for Physics
**Date:** 2025-01
**Status:** Accepted
**Rationale:** JIT + x64 + vmap.
**Rejected alternative:** NumPy (slow), PyTorch (heavy).

## ADR-003: numba for Detection
**Date:** 2025-01
**Status:** Accepted
**Rationale:** 100x faster than pure Python.
**Rejected alternative:** Cython (complex).

## ADR-004: uvloop + orjson
**Date:** 2025-01
**Status:** Accepted
**Rationale:** 2-10x faster.
**Rejected alternative:** asyncio + json (slow).

## ADR-005: No Risk Management
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Risk solved by geometry.
**Rejected alternative:** stop-loss, position limit.

## ADR-006: Time = Tick
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Natural quantization of markets.
**Rejected alternative:** seconds, candles.

## ADR-007: G_DEFAULT = 1e-6 for log-price positions
**Date:** 2026-10-07
**Status:** REJECTED
**Rationale:** VIOLATES Axiom 4 (self-induced gravity without free parameters).
**Rejected alternative:** N/A — this ADR is rejected.
**Rejection rationale:** See CON-001 in Conflicts.md. G must be self-derived from the system geometry, not a magic constant.
**Post-rejection action:** G_eff = 1 / <d²>_t (time-averaged squared distance).

**Note:** A prior documentation pass mistakenly recorded that the virial test I4
threshold had been "loosened to 1e-5" to make tests pass (CON-002). That never
occurred: `test_virial_ratio_convergence` always used the invariant criterion
`|<T>/<V> + 0.5| < 0.2` over a conservative two-body subsystem for 20,000 ticks
with dt = 0.001. CON-002 was a log-writing error, not a threshold change; the
entry has been corrected in Conflicts.md.

## ADR-008: Tangential velocity of 1D states from self-induced gravity (rigid rotation)
**Date:** 2026-10-10
**Status:** Accepted
**Supersedes:** the undocumented constant `0.25·sign(v)` in `_stabilized_state` (Conflicts.md CON-004)
**Decision:** A 1D state (bodies on the x-axis) is embedded in the orbital plane as a rigid rotation about the centre of mass:
- G = 1/<d²>, <d²> = (1/N) Σ_{i<j} |x_i − x_j|²  (Physics.md §Self-Induced Gravity)
- x̄ = Σ m_i x_i / Σ m_i
- ω² = − Σ_i a_i (x_i − x̄) / Σ_i (x_i − x̄)², where a_i = −Σ_{j≠i} G m_j (x_i − x_j)/|x_i − x_j|³
- v_y,i = ω (x_i − x̄)
**Rationale:** ω is the least-squares solution of the force balance a_i = −ω²(x_i − x̄). It is exact for two bodies (circular orbit) and has no free parameter (Axiom 4). The transverse velocity is a function of geometry only.
**Rejected alternatives:**
- Constant `0.25·sign(v)` (undocumented external parameter; violates goal.md).
- Same-direction transverse velocity `v_y = +√(G M/r̄)` for all bodies: measured to break energy conservation (E: 0.01 → 282) and the virial test.
- Heuristic `r̄ = √<d²>` in a Kepler formula: not derived from the force balance.
- Removing the 1D path entirely: requires rewriting the virial test; not chosen.
**Consequences:**
- For 1D input, L is a constant rotational value (≈ 0.707 for the 2-body test), not zero. The test comment was corrected; the threshold L_max < 1.0 is unchanged.
- For N ≥ 3 a single rigid ω is an approximation (no exact rigid equilibrium for general 3-body configurations). The residual is not measured yet.
- Only affects the 1D embedding path; 2D/3D inputs are unchanged.
**Verification (2026-10-10):** all 9 tests pass in default float64 configuration. Two-body virial test: |⟨T⟩/⟨V⟩ + ½| = 0.055 (20k ticks), 0.0054 (200k ticks). Energy relative drift ≈ 4e-8 over 20k ticks at dt = 0.001.

## ADR-009: Implementation language and tooling for the physics engine
**Date:** 2026-10-10
**Status:** Accepted
**Decision:** Keep Python 3.11 + JAX (float64) for `physics_jax`. Do not introduce another language (C/C++/Rust/Julia) now. Numba stays reserved for detectors as already stated in ADR-003.
**Rationale:** Measured on the sandbox (2 CPU cores, JAX 0.10.2): `symplectic_step` inside `lax.scan` runs at ≈ 3.3 M ticks/s. 10 M ticks (Phase 5) ≈ 3 s. No performance requirement in the docs is violated.
**Full analysis:** docs/ToolSelection.md (5 Whys).
**Revisit when:** live WebSocket ingestion (Phase 1) or the market-maker loop (Phase 4) show a measured bottleneck.
