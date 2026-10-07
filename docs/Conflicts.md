# Conflicts

## Status: Active conflicts require resolution.

## CON-001: ADR-007 G_DEFAULT violates Axiom 4
**Date:** 2026-10-07
**Files:** `docs/Decisions.md` (ADR-007) vs `docs/Axioms.md` (Axiom 4)
**Description:** ADR-007 introduced G_DEFAULT = 1e-6 as a magic constant for log-price positions. This violates Axiom 4 which requires self-induced gravity without free parameters.
**Severity:** HIGH
**Resolution proposed:** Reject ADR-007. Implement G_eff = 1 / <d²>_t (time-averaged squared distance). Update Physics.md with self-induced gravity formula.
**Status:** RESOLVED — ADR-007 rejected, Physics.md updated.

## CON-002: Virial test threshold loosening
**Date:** 2026-10-07
**Files:** `src/physics_jax.py` tests vs `docs/Invariants.md` (I4)
**Description:** The virial test threshold was loosened to 1e-5 to make tests pass. Invariants.md specifies |V + 0.5| < 0.2 for I4. The generalized virial theorem must be implemented.
**Severity:** MEDIUM
**Resolution proposed:** Implement generalized virial theorem (see Physics.md). If test still fails, log as falsification in FailureModes.md.
**Status:** OPEN

## Conflict Resolution Rules
1. If conflict with Philosophy → Philosophy wins.
2. If conflict with Axioms → Axioms wins.
3. If conflict with AI_Protocol → AI_Protocol wins.
4. Otherwise, escalate to human.

## History
| Date | Conflict | Resolution |
|------|----------|------------|
| 2026-10-07 | CON-001: G_DEFAULT violation | ADR-007 rejected |
