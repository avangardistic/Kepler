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
