# Conflicts

## Status: Active conflicts require resolution.

## CON-001: ADR-007 G_DEFAULT violates Axiom 4
**Date:** 2026-10-07
**Files:** `docs/Decisions.md` (ADR-007) vs `docs/Axioms.md` (Axiom 4)
**Description:** ADR-007 introduced G_DEFAULT = 1e-6 as a magic constant for log-price positions. This violates Axiom 4 which requires self-induced gravity without free parameters.
**Severity:** HIGH
**Resolution proposed:** Reject ADR-007. Implement G_eff = 1 / <d²>_t (time-averaged squared distance). Update Physics.md with self-induced gravity formula.
**Status:** RESOLVED — ADR-007 rejected, Physics.md updated.

## CON-002: Virial test threshold loosening (resolved)
**Date:** 2026-10-07
**Files:** `src/physics_jax.py` tests vs `docs/Invariants.md` (I4)
**Description:** Workflow confusion: an earlier migration pass log stated that the test
threshold was "loosened to 1e-5" to make tests pass. That never happened in the
codebase. `test_virial_ratio_convergence` has always evaluated I4 as
`|<T>/<V> + 0.5| < 0.2` (the invariant criterion from Invariants.md) over a
20,000-tick conservative two-body subsystem with dt = 0.001. The log entry was a
writing error, not a threshold change.
**Severity:** MEDIUM (log accuracy only; no code or invariant threshold changed)
**Resolution:** Log corrected. Invariants.md now documents both the standard virial
form (I4) for conservative subsystems and the generalized form (I4b) for systems
with external forces and friction. Physics.md documents the generalized form and
notes when each applies. The test remains unchanged and passes.

## CON-003: Energy test precision (float32 vs I2 criterion)
**Date:** 2026-10-10
**Files:** `src/physics_jax.py` (JAX default precision) vs `docs/Invariants.md` (I2, relative drift < 1e-9) and `docs/Decisions.md` (ADR-002: "JIT + x64 + vmap")
**Description:** Under JAX's default float32, `test_energy_conservation_relative_drift` fails with max relative energy drift 8.01e-08 (float32 eps ≈ 1.2e-7 cannot meet 1e-9). With `JAX_ENABLE_X64=1` all 9 tests pass. The ResearchLog entry of 2026-10-07 stated "absolute drift < 1e-5", which does not match the I2 criterion.
**Severity:** HIGH (test failing on default configuration)
**Resolution:** x64 enabled in `physics_jax.py` via `jax.config.update("jax_enable_x64", True)`, as prescribed by ADR-002. Verified: 9/9 tests pass without environment variables.
**Status:** RESOLVED — 2026-10-10. Correction logged in ResearchLog.md and Changelog.md.

## CON-004: Undocumented transverse velocity injection (RESOLVED)
**Date:** 2026-10-10
**Files:** `src/physics_jax.py` `_stabilized_state` (previously `v_y = 0.25·sign(v_x)`) vs `docs/goal.md` ("All parameters derived internally from geometry", "No external parameters").
**Description:** The constant `0.25` was not derived from geometry and was not documented. It also produced a non-zero angular momentum (≈ 0.5) while the test comment claimed L ≈ 0. Removing it outright broke `test_virial_ratio_convergence` (⟨T⟩/⟨V⟩ ≈ −252400).
**Human decision:** Derive the transverse velocity from geometry (option 2). Chosen 2026-10-10 by the project owner; formula chosen under the instruction to "use the most precise formulas".
**Resolution:** Rigid rotation about the mass centre with ω fitted to the self-induced gravity (ADR-008, Physics.md §Embedding). Constant removed. Test comment corrected; threshold unchanged. All 9 tests pass.
**Status:** RESOLVED — 2026-10-10.

## CON-005: Self-induced G normalisation mismatch (RESOLVED, one open remark)
**Date:** 2026-10-10
**Files:** `src/physics_jax.py` `compute_self_induced_G` (divided by the number of pairs) vs `docs/Physics.md` §Self-Induced Gravity (divides by N, the number of bodies).
**Description:** The two normalisations are identical for N = 3 (the target three-asset system) and differ for N = 2 (test-only subsystem). Measured: if the rotation used the Physics.md G while `integrate` used the code G, the two-body virial test failed (⟨T⟩/⟨V⟩ ≈ −2.39 over 200k ticks), because the velocities and the forces were computed with different couplings.
**Resolution:** Code aligned to Physics.md (1/N) in one shared helper `_self_induced_G_from_positions`, used by both the rotation and `compute_self_induced_G`. Consistency verified: two-body virial test passes.
**Status:** RESOLVED — 2026-10-10.
**Open remark (not changed):** Physics.md specifies a running time-average of ⟨d²⟩_t. The code uses the value from the initial state, held fixed in `integrate` (documented in its docstring). This is a known gap and needs a decision if the running average is required.

## Conflict Resolution Rules
1. If conflict with Philosophy → Philosophy wins.
2. If conflict with Axioms → Axioms wins.
3. If conflict with AI_Protocol → AI_Protocol wins.
4. Otherwise, escalate to human.

## History
| Date | Conflict | Resolution |
|------|----------|------------|
| 2026-10-07 | CON-001: G_DEFAULT violation | ADR-007 rejected |
| 2026-10-07 | CON-002: Virial test threshold loosening (log error) | Corrected log entry; test + invariants unchanged |
| 2026-10-10 | CON-003: Energy test fails under float32 | RESOLVED — x64 enabled (ADR-002) |
| 2026-10-10 | CON-004: Undocumented 0.25 transverse velocity constant | RESOLVED — rigid rotation from geometry (ADR-008) |
| 2026-10-10 | CON-005: G normalisation (pairs vs N) | RESOLVED — aligned to Physics.md (1/N) |
