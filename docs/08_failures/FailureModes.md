# Failure Modes

## F1 — Jump-to-Zero Depth
**Scenario:** Order book depth drops to zero in a single tick.
**Response:** $m \to 0$, $\vec L \to 0$ → freeze.
**Severity:** Low (self-correcting).

## F2 — Cross-Exchange Divergence
**Scenario:** Binance and Coinbase diverge by 5%.
**Response:** Cross-asset gravity pulls toward equilibrium.
**Severity:** Medium (short-term).

## F3 — Exogenous Shock
**Scenario:** Major news event (Fed, hack).
**Response:** Outside L2 field → system blind.
**Severity:** High (unavoidable).

## F4 — Numeric Overflow
**Scenario:** $1/d^3$ as $d \to 0$.
**Response:** $\epsilon$ regularizer.
**Severity:** Low.

## F5 — Detector False Positive
**Scenario:** Iceberg misidentified.
**Response:** Effective mass error.
**Severity:** Low (transient).

## F6 — Tick Drop
**Scenario:** A single tick is lost.
**Response:** Wrong integration step.
**Severity:** Medium.

## F7 — Symplectic Drift
**Scenario:** Cumulative numeric error.
**Response:** Periodic projection onto constraint manifold.
**Severity:** Low.

## F8 — Virial Breakdown
**Scenario:** $T/V$ diverges from $-1/2$.
**Response:** System returns to equilibrium (for conservative subsystem).
**Severity:** Self-healing.
**Clarified 2026-10-07 (R-PHY-001):** per-tick $T/V = -\frac12$ holds only for
circular (≥2-D) orbits; for general eccentricity it holds for *time-averages
over integer periods* ($\langle T\rangle/\langle V\rangle$). A per-tick
deviation inside an elliptical orbit is not a breakdown. "Self-healing" applies
only when the trajectory is collision-resolved (F10) — otherwise the divergence
is a numerical artifact, not dynamics.

## F9 — Generalized Virial Test Failure
**Scenario:** Generalized virial theorem $|2\langle T \rangle + \langle V \rangle + \langle F_{ext} \cdot x \rangle + \langle F_{friction} \cdot x \rangle| > \text{threshold}$.
**Response:** Log as falsification in FailureModes.md. Do NOT loosen threshold.
**Severity:** Varies — may indicate model inadequacy.
**Status:** MONITORED

## F10 — Unresolved Close-Approach Heating (1-D "Orbit" Artifact)
**Added:** 2026-10-07 (Session 2), from R-PHY-001.
**Scenario:** A conservative test (or live 1-D sub-step) with bound
gravitating bodies in 1-D. Zero angular momentum ⇒ every bound orbit is a
radial plunge; separation collapses toward the ε=1e−8 softening core; velocity
spikes (|v| ~ 7e3 analytically at core scale) render the fixed-dt leapfrog
steps unresolved. Discrete-time scattering injects energy (measured:
E −0.115 → +296, pair escapes), and any time-averaged invariant (virial, energy)
computed on that trajectory measures the numerical fireball, not the model.
**Symptoms:** |⟨E⟩ jump| ≫ 1e−9·|E|; virial-like ratios converging to −1 (or
blowing up through the |V| < ε division guard, e.g. means of order −1e5).
**Response:** Do NOT touch thresholds and do NOT "compensate" the ratio. Reject
the *configuration*: any conservative invariant test must pass the
collision-resolution preflight of `06_research/physics/orbital_conditions.md`
(min sep ≥ C·dt·max|v|), or be defined in ≥2-D with an angular-momentum barrier
(circular orbit being the exact case).
**Severity:** HIGH for test validity; zero for the model (theorem survived —
it was the experiment that died).
**Related:** F4 (why ε exists), F8 (correct interpretation), F9, I2/I4.
