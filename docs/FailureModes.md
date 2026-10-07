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

## F9 — Generalized Virial Test Failure
**Scenario:** Generalized virial theorem $|2\langle T \rangle + \langle V \rangle + \langle F_{ext} \cdot x \rangle + \langle F_{friction} \cdot x \rangle| > \text{threshold}$.
**Response:** Log as falsification in FailureModes.md. Do NOT loosen threshold.
**Severity:** Varies — may indicate model inadequacy.
**Status:** MONITORED
