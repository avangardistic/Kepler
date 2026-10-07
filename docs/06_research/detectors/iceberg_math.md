# R-DET-001: Iceberg Detection Math

**Status:** NOT STARTED (framing only — this file defines what "started" means)
**Question:** Can iceberg replenishment be detected from orbital geometry
alone — mass `mᵢ = ln(1 + Σq)` and its derivatives — with **no filters,
no z-scores, no second-based lifetimes** (Philosophy §2.1–2.2, §2.4)?

## Why the inherited spec cannot be adopted
`04_market/Detectors.md` (still Persian, pre-protocol) defines
`score_ice = refills·(1−r_visible)·min(t/60, 1)` with thresholds
("refills ≥ 3, lifetime ≥ 5 s"). That formulation:
1. counts "refills" — requires order **identity** tracking that L2 snapshots
   do not provide (DataSpec.md: level arrays only);
2. uses wall-clock seconds — violates Axiom "time = tick" (ADR-006);
3. hard-codes 60 and 0.4 — external parameters (Philosophy §3).
It must be **re-derived**, not tuned. This is also F5's domain: a mis-modeled
iceberg is an error in the source of `mᵢ` itself, i.e. in the *gravitating
mass*, which propagates into every force — that is why detection belongs to
physics, not to indicators.

## Candidate geometric signatures (to formalize and test)
1. **Sub-Poisson depth fluctuation at fixed microprice.** Iceberg = visible
   fraction q_v constantly refreshed → level-k quantity variance at constant
   price collapses toward 0 while *trade* prints continue:
   `Var_τ(q_level k) → 0` but `μ_τ(print volume at that level) > 0`.
   Formalize via the tick-covariance `C_{qL}(Δt) = Cov(q_k(t), q_k(t+Δt))` —
   normal books decay, iceberg books show a floor.
2. **Mass inertia mismatch.** In `m = ln(1+Σq)`, an iceberg adds large true
   volume with small apparent volume → the body responds to `I` (drive)
   *too sluggishly* relative to its printed flow: mismatch
   `‖Δẍ_grav‖ expected from prints − measured ‖Δẍ‖`. Detection = model
   residual of the EOM, not a threshold on a score.
3. **Force-conservation residual.** Since all accelerations come from
   pairwise G mᵢmⱼ, hidden mass violates the internal consistency between
   relative acceleration of the three bodies and their *visible* masses;
   residual → effective-mass correction term (analogous to dark matter
   inference). A principled estimator: infer `m̂` from orbital dynamics
   (least-squares on one tick-window of the integrated EOM) and compare
   with book-derived `m`. `m̂ ≫ m` ⇔ hidden depth. This is the only
   filter-free definition consistent with the axioms.

## Required before R-DET-001 is "started"
- Write the estimators on synthetic two-state book generators (ice vs.
  natural replenishment), all quantities in ticks.
- Falsifiable criterion tied to `07_hypotheses/Falsifiability.md`; expected
  failure mode = F5 with quantified mass error.
- Only then touch `src/` (roadmap Phase 3 / T-005 depends on this file).

## Owner / next action
[unassigned] — Start by formalizing estimator (3); it doubles as a test of
Axiom 3 (mass ≡ depth) and would be falsified by any m̂–m correlation drift.
