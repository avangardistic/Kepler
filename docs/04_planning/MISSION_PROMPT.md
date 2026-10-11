# Kepler Mission Prompt

Use this as an onboarding prompt after reading the repository-level [`AGENTS.md`](../../AGENTS.md). It is a guide to the current checkout, not a substitute for source code, tests, or a maintainer decision.

## Mission

Test whether three-body dynamics on raw L2 order-book snapshots can describe selected market-microstructure behavior. This is an offline research project. It must not become a trading bot, signal/quote service, price predictor, risk-control replacement, or execution system.

## Read before changing code

1. [`goal.md`](goal.md) — objective, constraints, and anti-goals.
2. [`../01_theory/Axioms.md`](../01_theory/Axioms.md) and [`../01_theory/Invariants.md`](../01_theory/Invariants.md) — model claims and fixed criteria.
3. [`../03_research/Conflicts.md`](../03_research/Conflicts.md) — especially open CON-008.
4. [`TaskQueue.md`](TaskQueue.md) and [`roadmap.md`](roadmap.md) — planned work and dependencies.
5. Relevant implementation and tests; history is useful context, not the implementation source of truth.

For most tasks, read only the relevant sections instead of loading every document.

## Current repository facts

- **Phase 1 is implemented:** `src/fast_l2_client.py` ingests raw `depth20@100ms` snapshots; `src/tick_buffer.py` stores/replays them using Parquet.
- The recorded offline acceptance run covered 100,000 ticks with zero drops and ordering errors; a 2,785-tick live capture is committed under `tests/data/live_2026-10-11/`. A full 100,000-tick live run has not been recorded.
- **Physics code exists:** `src/physics_jax.py` implements a JAX three-body model. The recorded suite has 41 passing tests in its pinned environment, but those results do not establish real-data validity.
- **CON-008 is open:** the captured real-data replay violates the I1/I2 criteria in tested paths at `dt = 1`. Do not claim otherwise, tune thresholds, or pick a model resolution without the maintainer decision.
- **T-005 (detectors)** is data-unblocked and can be designed without the physics integration, but its draft must reconcile seconds-based thresholds with tick-time/no-filter constraints before implementation. **T-006** is blocked by a project-scope conflict. **T-007 / Phase 5** is blocked by CON-008 and the unfinalized `Π` experiment.
- Detector, quote-generation, and long-run simulation code are not implemented. A plan or mathematical sketch is not an implementation.

## Task rules

- Follow [`AI_Protocol.md`](AI_Protocol.md) and [`../02_engineering/QA_Protocol.md`](../02_engineering/QA_Protocol.md).
- Define the outcome, non-goals, and acceptance test before editing.
- Make the smallest coherent change; do not add speculative modules or dependencies.
- Preserve thresholds. Label synthetic, replay, and live evidence separately.
- Update the relevant spec/status when facts change. Record material research results in [`../03_research/ResearchLog.md`](../03_research/ResearchLog.md); record unresolved contradictions in [`../03_research/Conflicts.md`](../03_research/Conflicts.md).
- If a task requires changing project scope or a scientific assumption, stop at the decision point and ask the maintainer.

## Verification

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Report the actual command, environment, and outcome. If dependencies are unavailable, say so; never report the historical 41-test baseline as a test run in the current session.

## Finish

Review the complete diff, validate changed documentation links, and use [`AgentHandoff.md`](AgentHandoff.md) if work is incomplete. An unresolved, documented blocker is preferable to an invented resolution.
