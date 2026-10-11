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

> **Open conflict (CON-008).** I1 and I2 currently hold in the test suite but
> **fail on real replayed L2 data at `dt = 1` tick** (measured max relative
> energy drift 281 conservative, up to 6.2e6 with imbalance). The measurement,
> the structural causes and the candidate fixes are in Conflicts.md CON-008 and
> FailureModes.md F10. No threshold here has been changed, and no real-data
> invariant result may be reported as a pass until CON-008 is resolved.

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
| I6 | `test_physics.py`, `test_tick_buffer.py` | Always (`|I_i| ≤ 1`) |
| I7 | `test_fast_l2_client.py`, `test_tick_buffer.py` | `best_bid < best_ask` checked on every ingested tick and at construction |

## Phase 1 (tick infrastructure) guarantees

These are not physical invariants; they are the retention guarantees from
TaskQueue.md T-001/T-002, and they are tested in the default suite:

| Guarantee | Test | Criterion |
|-----------|------|-----------|
| No tick drops | `test_fast_l2_client.py` | `dropped == 0` over 100 000 ticks (Phase 1 exit criterion) |
| Arrival order | `test_fast_l2_client.py` | `out_of_order == 0`; `tick_index` contiguous |
| No filtering | `test_fast_l2_client.py` | malformed/empty books are delivered, only counted |
| Storage ordering | `test_tick_buffer.py` | `tick_index` strictly increasing, else `TickOrderError` |
| Field fidelity | `test_tick_buffer.py` | Parquet round trip is byte-exact per field and level |
| Deterministic replay | `test_tick_buffer.py` | identical tick sequence and identical `integrate` trajectory for the same dataset |
| No derived data | `test_tick_buffer.py` | only raw fields are stored; physics quantities are recomputed at replay |
