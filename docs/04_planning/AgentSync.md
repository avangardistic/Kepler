# Agent Synchronization

> Lightweight manual handoff only. This file is not a distributed lock or proof that an agent is still active. Update claims only when contributors actually coordinate on the same work.

**Last reviewed:** 2026-10-11

## Active claims

| Task / conflict | Contributor | Status | Last updated |
|---|---|---|---|
| None recorded | — | — | — |

Historical work and evidence are in [`../03_research/ResearchLog.md`](../03_research/ResearchLog.md); the backlog is [`TaskQueue.md`](TaskQueue.md).

## Current blockers and next work

- **CON-008:** open model decision. I1/I2 fail on the committed real-data replay at `dt = 1`; a maintainer decision and re-measurement are required before claiming real-data validation or proceeding to Phase 5.
- **T-005:** open and not blocked by Phase 1; detector work can use the recorded L2 data without relying on `integrate`.
- **T-006:** blocked pending a scope decision because quote generation conflicts with the project's anti-goals.
- **T-007 / Phase 5:** blocked by CON-008 and by the need to define `Π` and its experiment.

## Coordination rules

1. Check current source, tests, and conflicts before claiming work.
2. Add a time-limited claim only if there is real overlap risk; remove or close it at handoff.
3. Record blockers and evidence, not just status labels.
4. An open scientific conflict may be handed off; do not mark it resolved without a decision and verification.
5. External trackers are optional; see [`Paperclip_Coordination.md`](Paperclip_Coordination.md).
