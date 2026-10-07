# Conflicts

## Status: Active conflicts require resolution.

## CON-001: ADR-007 G_DEFAULT violates Axiom 4
**Date:** 2026-10-07
**Files:** `11_meta/Decisions.md` (ADR-007) vs `01_foundation/Axioms.md` (Axiom 4)
**Description:** ADR-007 introduced G_DEFAULT = 1e-6 as a magic constant for
log-price positions. This violates Axiom 4 which requires self-induced gravity
without free parameters.
**Severity:** HIGH
**Resolution proposed:** Reject ADR-007. Implement G_eff = 1 / <d²>_t
(time-averaged squared distance). Update Physics.md with self-induced gravity
formula.
**Status:** RESOLVED — ADR-007 rejected, Physics.md updated.

## CON-002: Virial test threshold vs Invariants.md I4
**Date:** 2026-10-07
**Files:** `tests/test_physics.py` vs `07_hypotheses/Invariants.md` (I4)
**Description:** The virial test threshold had been loosened to 1e-5 in an
earlier attempt to make tests pass. Invariants.md specifies
|⟨T⟩/⟨V⟩ + 0.5| < 0.2 for I4, and the generalized virial theorem must be
implemented for driven/damped systems. Test measured "T/V → −1.0".
**Severity:** MEDIUM
**Resolution proposed:** Implement generalized virial theorem (see Physics.md).
If test still fails, log as falsification in FailureModes.md. Do NOT loosen
threshold.
**Status:** RESOLVED — 2026-10-07 (Session 2). Resolution record:
1. Threshold restored to exactly 0.2 and never touched again (QA P3).
2. Root cause documented in `06_research/physics/virial_theorem.md`:
   (a) the 1-D initial conditions are unphysical for a circular-orbit claim —
   every 1-D bound orbit is a radial plunge whose close approaches are
   unresolved by fixed-dt leapfrog → numerical heating → escape (F10);
   (b) the old test bound integrate()'s 3rd return value (the per-tick virial
   RATIO) to a name `V`, computed "T = E − V", and reported
   mean(E−v̄)/mean(v̄) = Ē/V̄ − 1 ≈ −1.0008 — an algebraic artifact, not data.
3. Test rebuilt on an exactly-derivable 2-D circular orbit (v = 0.25 per body,
   self-consistent G = 1/⟨d²⟩ = 0.25): per-tick AND time-averaged
   |T/V + 0.5| asserted < 0.2; measured deviations ~1e-10.
4. Engine: isotropic (radial) softening ‖dx‖² + ε² for multi-D states
   (enabler; 1-D results bit-identical).
5. Harness: float64 enabled in `tests/conftest.py` — a precision setting for
   I2's 1e-9 threshold, not a threshold change.
6. Generalized virial theorem derived and documented
   (`06_research/physics/generalized_virial.md`); its I≠0, γ≠0 test is
   assigned T-008 in `12_prompts/TaskQueue.md`.
**Evidence:** 9/9 tests pass (2026-10-07); docs cited above.

## CON-003: G fallback constant in degenerate geometry
**Date:** 2026-10-07 (opened by Session-2 audit)
**Files:** `src/physics_jax.py::compute_self_induced_G` vs
`01_foundation/Axioms.md` (Axiom 4)
**Description:** When mean pairwise squared distance < ε (co-located or empty
books), the engine returns G = 1.0 — an unlogged magic constant, structurally
identical to the rejected ADR-007. Physics.md's formula 1/⟨d²⟩ is simply
undefined there. Related spec divergence: Physics.md says G_eff uses a
"running average over recent ticks" while `integrate()` freezes G from the
initial state — two different dynamical systems (see R-PHY-002).
**Severity:** LOW-MEDIUM (no test hits the branch; the frozen-vs-running
divergence blocks the general wording of H2/I2)
**Resolution options (human/ADR decision — Axioms are human-only):**
(a) G = 1/ε (continuous limit of the formula);
(b) G = 0 (co-located ⇒ no gravitational degree of freedom — matches the
    existing "single body ⇒ no gravity" branch);
(c) keep 1.0 and register it as an explicit, justified axiom amendment.
**Status:** OPEN — do not silently change the engine; decide, then update
Physics.md and (if needed) Decisions.md.

## Conflict Resolution Rules
1. If conflict with Philosophy → Philosophy wins.
2. If conflict with Axioms → Axioms wins.
3. If conflict with AI_Protocol → AI_Protocol wins.
4. Otherwise, escalate to human.

## History
| Date | Conflict | Resolution |
|------|----------|------------|
| 2026-10-07 | CON-001: G_DEFAULT violation | ADR-007 rejected |
| 2026-10-07 | CON-002: virial test vs I4 | RESOLVED — test rebuilt on 2-D circular orbit (R-PHY-001), F10 logged, generalized theorem derived |
| 2026-10-07 | CON-003: G fallback 1.0 + frozen-vs-running G | OPEN — ADR decision required (options a/b/c) |
