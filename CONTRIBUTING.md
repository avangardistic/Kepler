# Contributing to Kepler

This is a **research project, not a trading system**. Every change must preserve the scientific invariants and the project's constraints.

## Quick Start for Contributors

1. **Read the navigation hub:** [`docs/README.md`](docs/README.md) — pick the right doc for your task.
2. **Read the constraints:** [`docs/goal.md`](docs/goal.md) (only raw L2 ticks, time = ticks, no external params) and [`docs/Axioms.md`](docs/Axioms.md).
3. **Know the invariants:** [`docs/Invariants.md`](docs/Invariants.md) — I1–I7 + Phase-1 retention guarantees. Tests enforce them.
4. **Install:** `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
5. **Verify:** `pytest tests/ -v` must be **41/41** before you commit.

## Workflow (from `docs/QA_Protocol.md`)

- **Invariant-first (P1):** every code change preserves `Invariants.md`.
- **Falsification-first (P2):** if a test fails, question the model, not the threshold.
- **No threshold laziness (P3):** do not loosen thresholds to make tests pass.
- **Reproducibility (P4):** tests are offline, deterministic, injected clock/transport.

### Per-Change Checklist (QA_Protocol)

- [ ] `pytest tests/ -v` passes
- [ ] No invariant violated, no threshold loosened
- [ ] Documentation updated (`docs/README.md` if a doc was added/moved)
- [ ] `docs/ResearchLog.md` and `docs/Changelog.md` updated
- [ ] `docs/Conflicts.md` updated if a conflict was opened/resolved
- [ ] `docs/Decisions.md` updated if an ADR was added/superseded
- [ ] Change report follows [`CHANGES_TEMPLATE.md`](CHANGES_TEMPLATE.md) (link it in the PR description)

## Project Structure

```
Kepler/
├── docs/README.md       # Navigation hub (7.8 KB, categorised index of all 48 docs)
├── docs/INDEX.md        # Alias of README.md
├── CHANGES_TEMPLATE.md  # PR / session change-report template
├── src/
│   ├── fast_l2_client.py  # T-001: raw L2 WebSocket ingestion (pull, no drops)
│   ├── tick_buffer.py     # T-002: Parquet + zstd buffer & replay
│   └── physics_jax.py     # Phase 2: three-body engine (JAX float64, symplectic)
├── tests/               # 41 tests, offline & deterministic
└── requirements.txt
```

## Documentation

- Flat `docs/*.md` for now (48 files). Categorised view is `docs/README.md §Document Organisation`.
- A future reorganisation into `01_theory/ … 05_reference/` is planned but deferred until CON-008 is resolved (to avoid mixing model and doc moves). See `docs/README.md`.
- Every internal link uses `docs/<name>.md` until a reorg PR lands with a redirect shim.

## Code Style

- Python 3.11, type hints, docstrings.
- `__all__` lists only public API (`_helpers` are private by convention — see `src/fast_l2_client.py`).
- Empty books are the self-freeze case (Falsifiability F2): they return `0.0` with a `logger.debug`, not a warning — enable `logging.DEBUG` to observe.
- No `time.sleep` in the hot path, no `pandas`, no `threading.Lock`, no unbounded memory.

## Reporting Changes

Use [`CHANGES_TEMPLATE.md`](CHANGES_TEMPLATE.md) for every PR:

- **Changes Made** — code / docs / infra, each with reasoning (which ADR / conflict motivated it).
- **Policy Alignment** — invariants, thresholds, tests, constraints checklist.
- **Tests & Evidence** — `pytest` tail, measurements, live capture if applicable.
- **Conflicts & Risks** — introduced / resolved.

## Escalation

If QA cannot be resolved: document in `docs/Conflicts.md`, notify via `docs/AgentSync.md`, escalate to human (per `Conflicts.md §Conflict Resolution Rules`).

## Tests

```bash
# from the repo root
pytest tests/ -v                     # 41 tests
python -m src.fast_l2_client --ticks 100000 --out data/l2 --base wss://data-stream.binance.vision/stream
```

See `docs/DataSpec.md` and `docs/Implementation.md` for feed and storage details.
