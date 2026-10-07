# R-PHY-002: Self-Induced Gravity Derivation

**Status:** OPEN (Session 2 findings recorded; decision required — human/ADR)
**Question:** Is `G_eff = 1/⟨d²⟩_t` the right realization of Axiom 4, and in
which sense does the code implement it?

## What the code actually does (audited 2026-10-07)
`compute_self_induced_G()` computes `G = 1 / mean_pairwise(‖dx‖²)` from the
**initial** state, and `integrate()` **freezes it for the whole trajectory**.
`03_physics/Physics.md` claims a *running average over recent ticks*.
These are different dynamical systems:

| Property | frozen G (impl) | running G (Physics.md text) |
|---|---|---|
| Hamiltonian / symplectic | ✅ yes | ❌ no (explicitly time-dependent coupling) |
| I2 "E = const to machine precision" | ✅ testable | ❌ violated by construction |
| Axiom 4 "self-consistent adaptation" | only at t=0 | literal reading |

**This spec↔impl divergence is not yet a bug — it is the open decision.**
Either the theorem set (I2, standard virial) must be restricted to the frozen-
G subsystem, or a time-dependent-G invariant (generalized, R-PHY-004) must
replace them. Proposed as ADR-008 candidate; also candidate conflict CON-003
below.

## Properties of G_eff = 1/⟨d²⟩ (why it is defensible)
Let positions live in ln-microprice space, so `d` is dimensionless and
`G = 1/⟨d²⟩` is a pure number — no units, no free constant, positive definite,
and **scale-seeking**: pairs closer than unit log-distance interact strongly,
farther pairs interact weakly (force ∝ G·m/d² = m/d⁴ at the pair level for a
single pair — one power steeper than Newton). Consequences to examine:

1. **Effective exponent.** Substituting G_eff into the pair potential gives
   V_pair ∝ −1/(⟨d²⟩·d). For a single pair with ⟨d²⟩ = d² this is
   V ∝ −1/d³ — a *steeper-than-Kepler* potential. The standard virial ratio
   for homogeneous V ∝ rⁿ is ⟨T⟩/⟨V⟩ = n/2, i.e. **−3/2 for n = −3, not −1/2.**
   → Any H2-style claim must pin down whether ⟨d²⟩ is the *same* d that enters
   the force law. The current test (R-PHY-001) dodges this entirely because a
   circular orbit keeps d ≡ d₀, so frozen G = instantaneous G and the orbit is
   a genuine Kepler (n = −1) orbit under that constant G. Non-circular
   configurations do NOT dodge it.
2. **Degenerate guards.** `compute_self_induced_G` returns the magic value
   `1.0` when mean d² < ε (single-body or co-located books) — this is a
   G_DEFAULT in disguise and contradicts the CON-001 resolution. Should it
   instead return `1/ε` (the continuous limit) or 0 (decoupled)? NEEDS DECISION.
   Also `compute_virial_ratio` guards |V| < ε by substituting ε, which produced
   the giant spurious per-tick ratios documented in R-PHY-001 — the guard hides
   escape instead of reporting it.
3. **Noether charges.** A frozen G preserves translation symmetry → total
   momentum; running G is still translation-invariant but explicitly time-
   dependent → energy non-conservation is the expected channel, see R-PHY-004.

## Alternatives on the table (untested)
- `G = 1/⟨d²⟩_t` running average over a window W (W = ? ticks — window length
  would itself be an external parameter unless W = t, a causal cumulative mean).
- `G = c/⟨d⟩²` etc. — rejected without experiment (adds no symmetry).
- Keep frozen-initial G (current code) and *document Axiom 4 as an initial-
  condition calibration*: G is set by the first tick's geometry, then the game
  is conservative until the next "epoch". Simplest to reconcile with I2/I4.

## Proposed verification experiments (next sessions)
- E1: measure ⟨T⟩/⟨V⟩ for a 2-D *elliptical* orbit under (a) frozen G and
  (b) true running G. Prediction: (a) → −0.5 (R-PHY-001 table already shows
  it — because with d ≢ d₀ the *frozen* G is constant while ⟨d²⟩ varies; the
  deviation measured there was ~1e-8, so running-vs-frozen must be the
  discriminator, not eccentricity alone), (b) → systematic drift.
- E2: unit test pinning the degenerate-case G so the magic 1.0 is either
  justified in Conflicts.md or removed.

## Decision needed
Record outcome in `11_meta/Decisions.md` (new ADR) and update `Physics.md`,
`Axioms.md` untouched (human-only file).

## Status
OPEN — assigned next-session priority: HIGH (blocks the honest wording of H2
beyond circular orbits, and of I2 beyond the frozen-G subsystem).
