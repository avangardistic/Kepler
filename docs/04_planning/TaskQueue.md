# Task Queue

> The queue tracks planned work; code and tests define what is actually implemented. Do not infer approval for an out-of-scope feature from a task title.

## Current priority

1. **CON-008 decision:** a maintainer must choose the model direction and record an ADR before real-data I1/I2 claims or Phase 5. This is a decision gate, not a code task for an agent to settle unilaterally.
2. **T-005:** detectors can proceed on recorded raw ticks and do not depend on `integrate`.
3. **T-006:** blocked pending a scope decision about quote generation versus the anti-goals.
4. **T-007:** blocked by CON-008 and the need to define the mathematical `Π` experiment.

## Open

### T-005 — Phase 3 — Detectors

- **Status:** Open; Phase 1 data dependencies are met. Implementation is gated on clarifying the draft spec's seconds-based thresholds under tick-time and no-filter constraints.
- **Input:** [`../02_engineering/Detectors.md`](../02_engineering/Detectors.md), raw/replayed L2 data.
- **Output:** research-only offline annotations and tests; no trading signal service and no detector output fed back into the physics model as a filter.
- **Acceptance:** reproducible synthetic evaluation with F1 > 0.8, documented data generation and metric calculation; report separately from real-feed behavior. Treat the historical F1 target as provisional until the metric/data protocol is specified.
- **Blocked by:** None of T-001/T-002. Before code, reconcile time units and thresholds with the project constraints. Do not use a detector result as evidence for the physics model.

### T-006 — Phase 4 — Scope review for market-making proposal

- **Status:** Blocked pending an explicit maintainer decision.
- **Input:** [`../02_engineering/MarketMaking.md`](../02_engineering/MarketMaking.md), [`../01_theory/Strategy.md`](../01_theory/Strategy.md), and project anti-goals.
- **Output before any implementation:** reconcile the proposal with the no-signal/no-trading scope. If approved, define a strictly offline, non-actionable experiment and update the goal/ADR first.
- **Acceptance:** a written scope decision. Do not implement `quote_all`, emit actionable quotes, or connect it to execution while this conflict remains.

### T-007 — Phase 5 — Long-run model simulation

- **Status:** Blocked.
- **Input:** validated physics model, fixed experiment protocol, and stored/replayable data.
- **Output:** reproducible simulation report; no orders or realized-trading claims.
- **Acceptance:** define `Π`, population, baseline, and uncertainty procedure before running; CON-008 resolved and relevant real-data behavior re-measured. The historical “10M ticks, Π > 0 with 95% CI” line is a proposal, not a completed result.
- **Blocked by:** CON-008, prerequisite tasks/model decisions, and experiment definition.

## Completed

- [x] **T-000 — Phase 0:** initial documentation set created. Some theoretical claims remain unvalidated; see the current goal and research records.
- [x] **T-001 — Phase 1:** `src/fast_l2_client.py`, raw Binance `depth20@100ms` snapshots, order/back-pressure counters, and offline 100,000-tick acceptance test. A 2,785-tick live capture was recorded. Full 100,000-tick live acceptance remains unrun.
- [x] **T-002 — Phase 1:** `src/tick_buffer.py`, bounded buffer, Parquet/zstd store, and deterministic replay.
- [x] **T-003 — Phase 2:** `src/physics_jax.py`, JAX physics model and symplectic integration.
- [x] **T-004 — Phase 2:** physics tests in `tests/test_physics.py`.

The last repository-recorded suite result was **41 passed** with the pinned dependency set on 2026-10-11. It is historical evidence, not a claim that tests were run in the current session. Real-data I1/I2 failures remain recorded in CON-008/F10.

## Follow-ups / known limits

- `TickReplay.states()` was measured at about 76 states/s in the recorded environment because state construction is outside JIT. Optimize only after re-benchmarking and preserving outputs.
- `integrate` holds self-induced `G` from the initial state; the docs' running time-average description is not implemented (CON-005 remark).
- T-001's full live 100,000-tick run is outstanding; the committed fixture is smaller.
- Keep current changelog entries labelled correctly: the v0.2.0–v0.5.0 modules were planned, not delivered.
