# Invariants

## Fundamental Invariants

### I1 — Angular Momentum
$$
\frac{d\vec L}{dt} = 0 \quad \text{(no external torque)}
$$

### I2 — Total Energy
$$
E = T + V = \text{const} \quad \text{(closed system)}
$$

### I3 — Hedge Constraint
$$
\phi(h) = 0
$$

### I4 — Virial Ratio
$$
2\langle T \rangle + \langle V \rangle = 0
$$

### I5 — Total Mass
$$
\sum_i m_i = \text{const} \quad \text{(no volume exchange)}
$$

### I6 — Normalized Imbalance
$$
|I_i| \leq 1
$$

### I7 — Bid < Ask Constraint
$$
\text{Bid}_i < \text{Ask}_i
$$

## Tests
| Invariant | Test | Criterion |
|-----------|------|-----------|
| I1 | `test_physics.py` | Relative error < 1e-9 |
| I2 | `test_physics.py` | Same |
| I3 | `test_mm.py` | |φ| < 1e-6 |
| I4 | `test_physics.py` | |V + 0.5| < 0.2 |
| I5 | `test_sim.py` | drift < 1% |
| I6 | `test_detectors.py` | Always |
| I7 | `test_mm.py` | Always |
