# Contributing to Kepler

Kepler is an offline research project, not a trading system. Read [`AGENTS.md`](AGENTS.md) before changing code; it is the concise source for the repository-wide workflow and boundaries.

## Start

1. Read the documentation map: [`docs/README.md`](docs/README.md).
2. Confirm scope in [`docs/04_planning/goal.md`](docs/04_planning/goal.md), relevant axioms/invariants, and open conflicts.
3. Inspect the actual source and tests before relying on historical docs or task status.
4. Create/activate a Python 3.11 virtual environment and install `requirements.txt`.
5. Run focused tests while iterating; run the full suite before describing a code change as verified.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

## Working rules

- State an observable outcome, non-goals, and acceptance criterion before implementation.
- Make the smallest complete change. Avoid speculative modules and unnecessary dependencies.
- Never add exchange execution, actionable quotes, trading signals, or risk-safety claims.
- Preserve invariant thresholds. A proposed scientific criterion change requires an explicit decision and rationale.
- Distinguish synthetic tests, offline replay, and live-feed evidence. Do not present one as another.
- If a model/scope decision is unresolved, document the options and blocker instead of guessing. CON-008 remains open; T-006 is blocked by a separate scope question.
- Update only the docs whose facts or decisions changed. Record material research evidence and notable user-facing changes; do not churn history for a typo fix.
- Optional external trackers are not assumed. See [`docs/04_planning/Paperclip_Coordination.md`](docs/04_planning/Paperclip_Coordination.md).

## Project structure

- `src/` — implemented Python modules.
- `tests/` — offline deterministic tests and a committed live-data fixture.
- `docs/01_theory/` — model vocabulary and claims.
- `docs/02_engineering/` — data, architecture, decisions, QA.
- `docs/03_research/` — hypotheses, experiments, conflicts, evidence, history.
- `docs/04_planning/` — scope, roadmap, task queue, prompts, coordination.
- `docs/05_reference/` — glossary, notation, references.

The canonical docs are in those categorized folders. Flat `docs/<name>.md` files are compatibility stubs; edit the canonical file and update the index if adding/moving docs.

## Reporting

For a substantial change, use [`CHANGES_TEMPLATE.md`](CHANGES_TEMPLATE.md). Include the exact tests/commands and outcomes, any unverified behavior, conflicts, and follow-up. A commit or external post is not a substitute for evidence.
