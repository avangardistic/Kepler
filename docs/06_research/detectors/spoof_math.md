# R-DET-002: Spoof Detection Math

**Status:** NOT STARTED (framing only)
**Question:** Can spoofing (large far-from-mid orders placed to induce a
false potential gradient, cancelled before trade) be detected as a *dynamical*
property of the mass field rather than a cancel-rate statistic?

## Inherited spec's problems (same audit as R-DET-001)
`Detectors.md` spoof score uses z-score, cancel/fill ratio, bps distance,
seconds-based age, and an exponential `e^{−d/100}` — indicators + wall-clock
+ magic constants. Not admissible; must be re-derived geometrically.

## Geometric view of a spoof
A spoof is a **pulsed, non-Keplerian mass perturbation**: it enters `m` and
`Σq` instantly, perturbs every other body's acceleration through
`G m_i m_j/d³`, and vanishes without exchanging momentum via trades.
Legitimate depth changes propagate through microprice motion `ẋ` and
imbalance `I`; a pure cancellation changes `m` with **no matching impulse
in the momentum ledger** (no trades, no queue-position decay of the level).

Candidate signatures (formalize in tick units, no thresholds from outside):
1. **Mass-jump / action-conservation residual.** Between ticks, compare
   `Δm_i` against the impulse implied by trade prints at that body's book.
   Spoof: `|Δm| ≫ impulse mass moved`. Quantify as the violation of the
   EOM's mass-source consistency across a whole 3-body window — one scalar,
   shared with R-DET-001 estimator (3).
2. **Curvature anomaly in the γ channel.** Spread/friction `γ = spread/x`
   spikes when far levels appear (they widen effective distance statistics?)
   — weak; keep as secondary.
3. **Larmor-like radiation analogy:** accelerating a test body by moving a
   source mass in and out with no transport is like driving the field
   without injecting momentum; measure `Σᵢ ∮ Fᵢ·dxᵢ` over a tick window —
   a conservative book change leaves the closed-loop work ≈ 0; pulsed
   spoofing injects net loop work. Connects to H3 (Π = ∮p·dx).

## Required before "started"
Same gate as R-DET-001: synthetic spoof generator + geometry-only estimators
+ a rejection criterion written into `07_hypotheses/` first. Falsification
mode to watch: a legitimate market-maker requote pattern triggers it
(that would be a genuine model failure — log under F5/F9).

## Owner / next action
[unassigned] — jointly scope estimators (1)+(3) with R-DET-001 (they share
the mass-source-consistency primitive; build once).
