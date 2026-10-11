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

For one-dimensional input, bodies are embedded in the orbital plane as a rigid rotation about the centre of mass, with ω derived from the self-induced gravity (see [`docs/Decisions.md`](docs/Decisions.md) ADR-008 and [`docs/Physics.md`](docs/Physics.md) §Embedding).

## Current status

The project follows the phases in [`docs/roadmap.md`](docs/roadmap.md).

| Area | Status |
|---|---|
| Phase 0: documentation | Done |
| Phase 1: tick infrastructure (`src/fast_l2_client.py`, `src/tick_buffer.py`) | Done — 100 000-tick acceptance run passes offline; a 2 785-tick live capture was recorded |
| Phase 2: physics engine (`src/physics_jax.py`) | Implemented; invariant tests pass on purpose-built configurations. **Real-data replay currently fails I2 — open conflict CON-008** |
| Phase 3: detectors | Not started (recorded ticks are now available) |
| Phase 4: market making | Not started |
| Phase 5+: simulation, validation, extensions | Not started, blocked by CON-008 |

Implemented in `src/fast_l2_client.py` (T-001):

- `FastL2Client`: raw `depth20@100ms` snapshot client for BTC/ETH/SOL. Pull-based `stream()` (a slow consumer pauses the reader, so ticks cannot be dropped), `stats` counters (`dropped`, `out_of_order`, `invalid_books`, `reconnects`, `last_error`), a blocking driver queue (`start()` / `pop_batch()`), and `install_event_loop_policy()`.
- `parse_message` / `L2Tick`: pure decoding that preserves level order and quantities verbatim, plus the DataSpec book-validation predicate.
- Live capture CLI: `python -m src.fast_l2_client --ticks 100000 --out data/l2`.

Implemented in `src/tick_buffer.py` (T-002):

- `TickBuffer`: bounded in-memory block, flushes to storage (no unbounded memory) and rejects non-increasing `tick_index`.
- `L2ParquetStore`: Parquet + zstd, partitioned `symbol=<S>/day=<YYYY-MM-DD>/part-NNNN.parquet`, part numbering continues across sessions.
- `TickReplay`: deterministic `ticks()` and `states()` (the latter feeds `state_from_l2`), plus `parquet_codecs()` for dependency-free codec verification.

Implemented in `src/physics_jax.py`:

- `ThreeBodyState`: JAX pytree holding positions, velocities, masses, imbalance and friction.
- `symplectic_step`, `integrate` (`lax.scan`), `acceleration`.
- Energy, potential, kinetic, virial ratio, angular momentum and self-induced G.
- `state_from_l2`: builds a state from three L2 books.

Test coverage (`pytest tests/ -v`, **41 tests**):

- `tests/test_physics.py` (9): angular momentum (zero at rest and bounded over 10k ticks), energy conservation, virial ratio (I4), imbalance bound (I6), zero-depth freeze, ε-softening, cumulative angular momentum, determinism.
- `tests/test_fast_l2_client.py` (17): order and counters, no-drop acceptance over 100 000 ticks, malformed/empty books not filtered, sequence-regression counting, reconnect without loss, back-pressure, and a real loopback WebSocket run.
- `tests/test_tick_buffer.py` (15): Parquet round-trip fidelity, partition layout and zstd codec (via the footer reader), ordering enforcement, auto-flush bounds, deterministic replay into `integrate`, filters and empty datasets.

All of them are offline and deterministic (injected clock/transport, `tmp_path` storage).

## Requirements

- Python 3.11 (validated version)
- `jax==0.10.2`, `pytest==9.1.1`, `websockets==17.2`, `orjson==3.13.0`, `polars==2.0.0` (see [`requirements.txt`](requirements.txt))
- `uvloop` is used when importable and skipped on Windows (ADR-010). `polars` is installed with the `[rtcompat]` extra on CPUs without AVX2 — the default runtime refuses to start there.

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

Run the commands from the repository root, because the tests import `src.*`.

Capture raw L2 ticks to Parquet (Phase 1):

```bash
# 100 000 ticks = the T-001 acceptance criterion.  The main Binance domain
# answers HTTP 451 in some regions; the .vision domain serves the same streams.
python -m src.fast_l2_client --ticks 100000 --out data/l2 \
    --base wss://data-stream.binance.vision/stream
```

Replay a dataset into the physics engine:

```python
from src.tick_buffer import TickReplay

for state in TickReplay("data/l2").states():   # one tick = one L2 update
    ...                                        # state is ready for integrate()
```

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

**Note:** total energy is conserved only for the conservative subsystem (no imbalance force, no friction). With non-zero imbalance `I` and friction `γ`, the energy returned by `integrate` is not constant, as expected from [`docs/Physics.md`](docs/Physics.md). On **real** replayed L2 books this is not a small effect: see [`docs/FailureModes.md`](docs/FailureModes.md) F10 and [`docs/Conflicts.md`](docs/Conflicts.md) CON-008.

## Repository layout

```
Kepler/
├── docs/                    # Theory, axioms, decisions, conflicts, research log
├── src/
│   ├── __init__.py
│   ├── fast_l2_client.py    # Phase 1: raw L2 WebSocket ingestion (T-001)
│   ├── tick_buffer.py       # Phase 1: buffer + Parquet + replay (T-002)
│   └── physics_jax.py       # Phase 2: three-body physics engine (JAX, float64)
├── tests/
│   ├── test_fast_l2_client.py
│   ├── test_tick_buffer.py
│   └── test_physics.py
├── requirements.txt
└── .gitignore
```

## Documentation

Start here:

- [`docs/goal.md`](docs/goal.md): goals, constraints and anti-goals
- [`docs/Concept.md`](docs/Concept.md): model definitions
- [`docs/Axioms.md`](docs/Axioms.md) and [`docs/Invariants.md`](docs/Invariants.md): axioms and invariants with test criteria
- [`docs/Physics.md`](docs/Physics.md): Lagrangian, energy, virial theorem, self-induced gravity
- [`docs/roadmap.md`](docs/roadmap.md) and [`docs/TaskQueue.md`](docs/TaskQueue.md): phases and open tasks
- [`docs/Decisions.md`](docs/Decisions.md): architecture decision records (ADR)
- [`docs/Conflicts.md`](docs/Conflicts.md): known conflicts and their resolution
- [`docs/ToolSelection.md`](docs/ToolSelection.md): why Python and JAX were kept, with measurements
- [`docs/DataSpec.md`](docs/DataSpec.md): L2 schema, Parquet layout and validation semantics
- [`docs/FailureModes.md`](docs/FailureModes.md): known failure modes, including F10 (real-data invariant failure)
- [`docs/prompt.md`](docs/prompt.md): entry prompt for a fresh agent session
- [`docs/ResearchLog.md`](docs/ResearchLog.md) and [`docs/Changelog.md`](docs/Changelog.md): history

## Known limitations

- **I1/I2 on real data (CON-008, open):** replaying live L2 books at `dt = 1` tick, the energy criterion I2 fails (max relative drift 281 conservative, up to 6.2e6 with imbalance); the ADR-008 rigid-rotation embedding is not applied to L2-built states because `state_from_l2` returns 2-D positions. Measured table in [`docs/FailureModes.md`](docs/FailureModes.md) F10. Needs a model decision before any Phase 5 result.
- **Coupling `G`:** `integrate` uses `G` from the initial state, held fixed. [`docs/Physics.md`](docs/Physics.md) describes a running time-average of ⟨d²⟩; this is not implemented yet (see [`docs/Conflicts.md`](docs/Conflicts.md) CON-005).
- **Three or more bodies:** the rigid-rotation embedding is exact only for two bodies. Its N ≥ 3 residual is now measured on real data (F10) and is large at `dt = 1`.
- **Live acceptance run:** the 100 000-tick criterion is verified offline; a live run takes ≈ 55 min at the observed ~23 ticks/s. A 2 785-tick live capture was recorded and replayed.
- **Feed availability:** `stream.binance.com` returned HTTP 451 from the verification network; `wss://data-stream.binance.vision/stream` serves the identical `depth20@100ms` payloads.
- **Scope:** detectors, market-making logic and simulation are not implemented yet. They do not exist in this repository.

## Contributing

Work follows the process in [`docs/QA_Protocol.md`](docs/QA_Protocol.md):

- Every change must preserve the invariants in [`docs/Invariants.md`](docs/Invariants.md).
- Test thresholds are fixed. Do not loosen them to make tests pass.
- Log state changes in [`docs/ResearchLog.md`](docs/ResearchLog.md) and conflicts in [`docs/Conflicts.md`](docs/Conflicts.md).

Run `pytest tests/ -v` before each commit.
