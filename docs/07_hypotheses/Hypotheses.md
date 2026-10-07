# Hypotheses

## H1 — Orbital Stability
**Claim:** $\|\vec L\|$ is bounded.
**Rejection criterion:** $\|\vec L\| > 10 \bar{L}$ in >5% of time.

## H2 — Virial Equilibrium (REVISED 2026-10-07, post R-PHY-001)
**Original claim:** $T/V \to -1/2$ (per tick, any bound orbit).
**Revised claim:** $\langle T\rangle/\langle V\rangle \to -1/2$ over time
averages spanning exact integer orbital periods for the **conservative
subsystem** ($I=0,\ \gamma=0$, frozen $G$); for circular orbits it holds
instantaneously at every tick. In the general case the testable statement is
the generalized identity $2\langle T\rangle + \langle V\rangle +
\langle\sum_i m_i I_i x_i\rangle - \langle\sum_i \gamma_i |v_i|^2\rangle = 0$
(`06_research/physics/generalized_virial.md`).
**Rejection criterion:** Deviation > 20% (0.2 absolute on the ratio) in 90% of
time — magnitude UNCHANGED from Invariants.md I4; only the averaged quantity
and the period/window rule are now specified.
**Status:** Passing in the circular-orbit regime (`test_virial_ratio_convergence`,
deviation ~1e-10). Generalization pending R-PHY-004/T-008.
**Evidence:** `06_research/physics/virial_theorem.md`, `FailureModes.md` F10.

## H3 — Profit = Curvature
**Claim:** $\Pi \propto \int \|\vec L\| dt$.
**Rejection criterion:** Correlation < 0.5.

## H4 — Freeze on Linear
**Claim:** $\|\vec L\| = 0 \Rightarrow Q = 0$.
**Rejection criterion:** Quoted volume in this state > 0.

## H5 — Recovery After Gap
**Claim:** After a gap, orbit returns to initial state.
**Rejection criterion:** No recovery within <10 ticks.

## H6 — Filter-Free Adaptation
**Claim:** System behaves correctly in all 10 L2 states.
**Rejection criterion:** Failure in ≥2 states.

## H7 — Hedge Invariance
**Claim:** $\phi(h) = 0$ always.
**Rejection criterion:** Deviation > 1e-6.
