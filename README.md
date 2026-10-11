# Kepler

Kepler is an offline research codebase testing whether three-body dynamics on raw Level 2 (L2) order-book snapshots can describe selected high-frequency market-microstructure behavior.

> **Research only. Not a trading system.** The repository does not place orders, issue actionable trading signals, predict prices, or establish realized profitability or financial safety.

## Research objective and boundaries

The project asks whether a geometric model is a useful descriptive language—not whether it can trade profitably. Only raw L2 snapshots are the modeled input; derived state is computed explicitly during replay. Time is counted in ticks. No hidden indicators, filters, or unexplained physical parameters may be introduced.

Key definitions and scope are in [`docs/04_planning/goal.md`](docs/04_planning/goal.md), [`docs/01_theory/Concept.md`](docs/01_theory/Concept.md), and [`docs/01_theory/Axioms.md`](docs/01_theory/Axioms.md).

## Current status

| Area | Status |
|---|---|
| Phase 1 — raw L2 ingestion, bounded storage, replay | Implemented. The offline 100,000-tick acceptance test and deterministic replay are recorded as passing. A 2,785-tick live capture is committed; the full 100,000-tick live run is outstanding. |
| Phase 2 — physics | `src/physics_jax.py` and synthetic invariant tests exist. **Real-data validation is not complete:** I1/I2 fail on the captured replay at `dt = 1`; see [CON-008](docs/03_research/Conflicts.md) and [F10](docs/03_research/FailureModes.md). |
| Phase 3 — detectors | Not implemented. T-005 is data-unblocked, but its draft seconds-based thresholds must be reconciled with tick-time/no-filter constraints before implementation. |
| Phase 4 — market-making proposal | Not implemented; T-006 is blocked by the conflict between quote generation and project anti-goals. No actionable output or execution is in scope. |
| Phase 5+ — simulation and extensions | Planned, not implemented. Phase 5 is blocked by CON-008 and by the need to define `Π` and its experiment. |

The latest repository-recorded test run was **41 passed** under the pinned environment on 2026-10-11. This is historical evidence, not a claim that tests have been run in the current checkout. See [`docs/03_research/ResearchLog.md`](docs/03_research/ResearchLog.md).

## Model overview

The current model maps three assets (BTC, ETH, SOL) to bodies in a state space based on log-microprice and L2 depth. These are modeling choices under test, not established physical quantities.

| Quantity | Current documented construction | Status |
|---|---|---|
| Position `x_i` | Log microprice | Implemented in the physics path; see [`docs/01_theory/Microprice.md`](docs/01_theory/Microprice.md) |
| Mass `m_i` | `ln(1 + depth)` | Model definition, not literal mass |
| Imbalance `I_i` | Normalized bid/ask depth difference | Model input/derived state |
| Coupling `G` | Self-induced from inter-body geometry | Current implementation holds the initial value fixed; the documented running-average form is unresolved (CON-005 remark) |
| Time | Discrete tick | Feed snapshots are asynchronous; replay uses latest-wins alignment |

The physics code uses a velocity-Verlet/symplectic integration path. Passing synthetic conservation tests does **not** show that invariants hold on real feed data; the current counterevidence is documented in CON-008/F10.

## Requirements and verification

The pinned environment recorded in the repository is Python 3.11, JAX 0.10.2, pytest 9.1.1, websockets 17.2, orjson 3.13.0, and polars 2.0.0. `uvloop` is optional. On CPUs unsupported by the standard Polars runtime, use the compatible runtime extra described in [`docs/02_engineering/Decisions.md`](docs/02_engineering/Decisions.md) ADR-011.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Run from the repository root. If dependencies cannot be installed or tests cannot run, report that rather than relying on the historical count.

## Capture and replay

Capture raw snapshots (requires network access to the public feed):

```bash
python -m src.fast_l2_client --ticks 100000 --out data/l2 \
    --base wss://data-stream.binance.vision/stream
```

The full live 100,000-tick acceptance run is not recorded as complete. The committed live fixture contains 2,785 ticks; its provenance and use are documented in `tests/data/live_2026-10-11/README.md`.

Replay stored snapshots locally:

```python
from src.tick_buffer import TickReplay

for tick in TickReplay("data/l2").ticks():
    ...  # raw fields are retained

for state in TickReplay("data/l2").states():
    ...  # derived model state; not stored as raw input
```

## Repository layout

```text
Kepler/
├── AGENTS.md                 # concise repository-wide agent instructions
├── README.md                 # project overview and quick start
├── CONTRIBUTING.md           # contributor workflow
├── CHANGES_TEMPLATE.md       # change/report template
├── docs/
│   ├── README.md             # canonical documentation map
│   ├── 01_theory/            # model and mathematical claims
│   ├── 02_engineering/       # implementation specs, decisions, QA
│   ├── 03_research/          # evidence, conflicts, history
│   ├── 04_planning/          # goals, roadmap, tasks, prompts/workflow
│   └── 05_reference/         # glossary, notation, references
├── src/
│   ├── fast_l2_client.py    # raw L2 WebSocket ingestion
│   ├── tick_buffer.py       # bounded buffer, Parquet store, replay
│   └── physics_jax.py       # JAX three-body physics path
└── tests/                    # offline tests and committed L2 fixture
```

Flat `docs/<name>.md` files are compatibility stubs pointing to the canonical categorized docs. Start at [`docs/README.md`](docs/README.md); do not edit the stubs.

## Known limitations

- **CON-008 / F10:** I1/I2 fail on tested real-data replay paths at `dt = 1`. The measured paths include energy drift 281 for the 2-D conservative path, 1.54 for the manually embedded conservative path, and larger drift with imbalance. The required I2 threshold is `< 1e-9`; no threshold has been loosened.
- **CON-005 remark:** `integrate` holds `G` from the initial state, while the theory document describes a running time average. This has not been resolved.
- **Embedding:** the rigid-rotation embedding is exact for two bodies; the general three-body residual is not a validated real-data solution.
- **Capture scale:** the committed real fixture has 2,785 ticks. The 100,000-tick no-drop acceptance result is offline/in-process, not a full-scale live run.
- **Unimplemented proposals:** detectors, quote/market-making output, long-run simulation, and validation experiments are not current code.

## Contributing

Follow [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`docs/02_engineering/QA_Protocol.md`](docs/02_engineering/QA_Protocol.md). Preserve fixed criteria, label evidence by data type, and keep known failures visible. The current task gates are in [`docs/04_planning/TaskQueue.md`](docs/04_planning/TaskQueue.md); the project map is [`docs/README.md`](docs/README.md).
