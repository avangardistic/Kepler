# Kepler

Three-body gravitational dynamics on Level 2 (L2) order-book tick data, used as a **descriptive language for high-frequency market microstructure**.

> **This is a research project, not a trading system.** It does not predict prices, generate signals, execute orders, or handle real money. See [Anti-goals](#anti-goals).

## Goal

The primary goal (from [`docs/goal.md`](docs/goal.md)) is to show that three-body gravitational dynamics on raw L2 tick data provide a useful descriptive vocabulary for HFT microstructure.

Success criteria:

1. Angular momentum ‖L‖ remains bounded.
2. Virial ratio T/V → −1/2.
3. Π > 0 in mathematical expectation.
4. Zero maximum drawdown (self-freeze).

### Constraints (immutable)

- Only raw L2 tick data as input.
- No external parameters, filters, indicators, or risk management.
- No execution, no real money, no profit claims.
- Time is quantised in ticks.
- All parameters are derived internally from geometry.

### Anti-goals

- Trading bot
- Signal generator
- Price prediction model
- Sellable strategy

## Model overview

Three assets are treated as three gravitational bodies in log-microprice space (see [`docs/Concept.md`](docs/Concept.md)):

| Quantity | Definition | Source |
|---|---|---|
| Position `x_i` | `ln P_i^μ` (microprice) | Concept §2.2 |
| Mass `m_i` | `ln(1 + total depth)` | Axiom 3, Concept §2.3 |
| Imbalance `I_i` | normalised bid/ask depth difference | Concept §2.4 |
| Gravitational coupling `G` | `G_eff = 1 / ⟨d²⟩` (self-induced) | Axiom 4, Physics §Self-Induced Gravity |

The integrator is a velocity-Verlet (symplectic) scheme, so energy and angular momentum are preserved without secular drift (see [`docs/Symplectic.md`](docs/Symplectic.md)).

For one-dimensional input, bodies are embedded in the orbital plane as a rigid rotation about the centre of mass, with ω derived from the self-induced gravity (see [`docs/Decisions.md`](docs/Decisions.md), ADR-008).

## Current status

The project follows the phases in [`docs/roadmap.md`](docs/roadmap.md).

| Area | Status |
|---|---|
| Phase 0: documentation | Done |
| Phase 2: physics engine (`src/physics_jax.py`) | Implemented; invariant tests pass |
| Phase 1: tick infrastructure (WebSocket client, tick buffer) | Not started |
| Phase 3: detectors | Not started |
| Phase 4: market making | Not started |
| Phase 5+: simulation, validation, extensions | Not started |

Implemented in `src/physics_jax.py`:

- `ThreeBodyState`: JAX pytree holding positions, velocities, masses, imbalance and friction.
- `symplectic_step`, `integrate` (`lax.scan`), `acceleration`.
- Energy, potential, kinetic, virial ratio, angular momentum and self-induced G.
- `state_from_l2`: builds a state from three L2 books.

Test coverage (`tests/test_physics.py`, 9 tests): angular momentum (zero at rest and bounded over 10k ticks), energy conservation, virial ratio (I4), imbalance bound (I6), zero-depth freeze, ε-softening, determinism.

## Requirements

- Python 3.11 (validated version)
- JAX `0.10.2` and pytest `9.1.1` (see [`requirements.txt`](requirements.txt))

The physics engine runs in double precision (`jax_enable_x64`), which is required by the energy criterion I2 (relative drift < 1e-9). See [`docs/Decisions.md`](docs/Decisions.md) ADR-002.

## Getting started

```bash
git clone https://github.com/avangardistic/Kepler.git
cd Kepler

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pytest tests/ -v
```

Run the commands from the repository root, because the tests import `src.physics_jax`.

Example: integrate a state built from three L2 books (one per asset):

```python
import jax.numpy as jnp
from src.physics_jax import state_from_l2, integrate

# Each side is a (K, 2) array of [price, quantity], best level first.
btc_bids = jnp.array([[99.95, 10.0], [99.90, 8.0]])
btc_asks = jnp.array([[100.05, 9.0], [100.10, 7.0]])
eth_bids = jnp.array([[200.10, 5.0], [200.00, 6.0]])
eth_asks = jnp.array([[200.30, 4.0], [200.40, 3.0]])
sol_bids = jnp.array([[50.00, 12.0], [49.95, 3.0]])
sol_asks = jnp.array([[50.02, 2.0], [50.10, 9.0]])

state = state_from_l2(btc_bids, btc_asks, eth_bids, eth_asks, sol_bids, sol_asks)
L_norm, energy, potential, imbalance = integrate(state, n_ticks=1000)
```

`G` is computed from the initial state when not given explicitly.

**Note:** total energy is conserved only for the conservative subsystem (no imbalance force, no friction). With non-zero imbalance `I` and friction `γ`, the energy returned by `integrate` is not the same as the Hamiltonian energy in the conservative subsystem.

## Repository layout

```
Kepler/
├── docs/              # Theory, axioms, decisions, conflicts, research log
├── src/
│   ├── __init__.py
│   └── physics_jax.py # Three-body physics engine (JAX, float64)
├── tests/
│   └── test_physics.py
├── requirements.txt
└── .gitignore
```

## Documentation

Start here:

- [`docs/prompt.md`](docs/prompt.md): entry prompt for a fresh agent session (read order and operating rules)
- [`docs/goal.md`](docs/goal.md): goals, constraints and anti-goals
- [`docs/Concept.md`](docs/Concept.md): model definitions
- [`docs/Axioms.md`](docs/Axioms.md) and [`docs/Invariants.md`](docs/Invariants.md): axioms and invariants with test criteria
- [`docs/Physics.md`](docs/Physics.md): Lagrangian, energy, virial theorem, self-induced gravity
- [`docs/roadmap.md`](docs/roadmap.md) and [`docs/TaskQueue.md`](docs/TaskQueue.md): phases and open tasks
- [`docs/Decisions.md`](docs/Decisions.md): architecture decision records (ADR)
- [`docs/Conflicts.md`](docs/Conflicts.md): known conflicts and their resolution
- [`docs/ToolSelection.md`](docs/ToolSelection.md): why Python and JAX were kept, with measurements
- [`docs/ResearchLog.md`](docs/ResearchLog.md) and [`docs/Changelog.md`](docs/Changelog.md): history

## Known limitations

- **Coupling `G`:** `integrate` uses `G` from the initial state, held fixed. [`docs/Physics.md`](docs/Physics.md) describes a running time-average of ⟨d²⟩; this is not implemented yet (see [`docs/Conflicts.md`](docs/Conflicts.md), CON-005).
- **Three or more bodies:** the rigid-rotation embedding is exact only for two bodies. For N ≥ 3 it is an approximation, and its residual has not been measured yet.
- **Scope:** only the physics engine is implemented. Live data ingestion, detectors, market-making logic and simulation are not part of this repository yet.

## Contributing

Work follows the process in [`docs/QA_Protocol.md`](docs/QA_Protocol.md):

- Every change must preserve the invariants in [`docs/Invariants.md`](docs/Invariants.md).
- Test thresholds are fixed. Do not loosen them to make tests pass.
- Log state changes in [`docs/ResearchLog.md`](docs/ResearchLog.md) and conflicts in [`docs/Conflicts.md`](docs/Conflicts.md).

Run `pytest tests/ -v` before each commit.
