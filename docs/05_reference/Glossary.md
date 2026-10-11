# Glossary

**Tick**: Smallest time unit. One L2 update.

**Level 2 (L2)**: Order book with multiple depth levels.

**Microprice**: Volume-weighted average of best bid/ask.

**Imbalance**: Normalized bid/ask depth difference.

**Iceberg**: Hidden order that replenishes repeatedly. (Detector concept only — no iceberg classifier is implemented; see `../02_engineering/Detectors.md`.)

**Spoof**: Large fake order that disappears without execution. (Detector concept only — not implemented.)

**Orbit**: Trajectory of three bodies in $(\ln P, m, I)$ space.

**Angular Momentum ($\vec L$)**: Measure of orbital rotation.

**Virial Ratio**: Ratio T/V that tends toward -1/2 in the conservative subsystem (I4).

**Symplectic**: Energy-preserving integrator.

**Hedge Constraint**: Mass ratio constraint between three assets.

**Model Mass**: $m_i = \ln(1 + \text{depth})$, a modeling choice, not a measured physical mass (Axiom 3). An iceberg/spoof-corrected variant is a detector proposal, not implemented.

**Spoof Score / Iceberg Score**: Detector-proposal metrics only; no scoring code exists (`../02_engineering/Detectors.md`).

**Π (work functional)**: Proposed mathematical functional (Axiom 7). It is not profit, P&L, or a profitability result.
