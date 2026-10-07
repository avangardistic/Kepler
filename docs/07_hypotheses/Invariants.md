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
> Scope note (2026-10-07): "const" is meaningful only for the conservative
> subsystem with **frozen G** (see R-PHY-002: running G would break it by
> construction). Verification additionally requires float64 — the 1e−9 bound
> lies below float32 machine epsilon (see `tests/conftest.py`).

### I3 — Hedge Constraint
$$
\phi(h) = 0
$$

### I4 — Virial Ratio
$$
2\langle T \rangle + \langle V \rangle = 0
$$
> Clarified 2026-10-07 (R-PHY-001 / H2 revision): the averages are
> time-averages over exact integer orbital periods of the conservative
> subsystem ($I=0,\gamma=0$, frozen $G$); per-tick $T/V\equiv-\tfrac12$ holds
> only for circular orbits. The threshold |⟨T⟩/⟨V⟩ + 0.5| < 0.2 is FIXED
> (QA P3) and requires float64 + a collision-resolved trajectory
> (`FailureModes.md` F10, preflight in `06_research/physics/orbital_conditions.md`).

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
