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

### I4 — Virial Ratio (Standard)
$$
2\langle T \rangle + \langle V \rangle = 0 \quad \Rightarrow \quad \frac{\langle T \rangle}{\langle V \rangle} = -\tfrac{1}{2}
$$

Applies to the **conservative subsystem** (no friction, no external forces).

### I4b — Virial Ratio (Generalized)
$$
2\langle T \rangle + \langle V \rangle + \langle \mathbf{F}_{ext} \cdot \mathbf{x} \rangle + \langle \mathbf{F}_{friction} \cdot \mathbf{x} \rangle = 0
$$

For systems with external forces and friction (Concept.md §3). The standard form
(I4) applies only to the conservative subsystem.

**Test criterion:** `test_virial_ratio_convergence` in `tests/test_physics.py`
computes the time-averaged ratio `<T>/<V>` after skipping an equilibration
period of 5,000 ticks and checks `|<T>/<V> + 0.5| < 0.2`. This matches the
I4 invariant criterion exactly. (A prior migration log entry claimed the test
threshold was "loosened to 1e-5" — that was a writing error; the test has
always used the I4 criterion above.)

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
| I4 | `test_physics.py` | |<T>/<V> + 0.5| < 0.2 (standard form for conservative subsystem; generalized form required when friction and external forces are present) |
| I5 | `test_sim.py` | drift < 1% |
| I6 | `test_detectors.py` | Always |
| I7 | `test_mm.py` | Always |
