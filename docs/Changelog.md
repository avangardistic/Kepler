# Agent Synchronization

## Active Agents
| Agent ID | Session Start | Current Task | Status |
|----------|--------------|--------------|--------|
| agent-main | 2026-10-07 | Phase 0: Documentation Migration | ✅ Complete |
| agent-main | 2026-10-10 | Phase 2: Verification and precision fix | ✅ Complete |
| agent-main | 2026-10-10 | Phase 2: Geometric embedding (ADR-008), tool decision (ADR-009) | ✅ Complete |
| agent-main | 2026-10-10 | Status audit and documentation sync (no code change) | ✅ Complete |

## Task Claims
| Task | Claimed By | Claimed At | Status |
|------|-----------|------------|--------|
| Phase 0 (all) | agent-main | 2026-10-07T10:00 | Done |
| T-003 (physics_jax) | agent-main | 2026-10-07 | Done — recorded in TaskQueue.md 2026-10-10 |
| T-004 (invariant tests) | agent-main | 2026-10-07 | Done — recorded in TaskQueue.md 2026-10-10 |
| T-001, T-002 | — | — | Unclaimed, highest priority |

## Recent Discoveries
- [2026-10-07T10:45] agent-main: G_DEFAULT violation found, ADR-007 rejected (CON-001)
- [2026-10-07T11:00] agent-main: Virial test needs generalized virial theorem (CON-002)
- [2026-10-07T11:05] agent-main: CON-002 corrected — no threshold loosening occurred; log entry was a writing error. Test always used I4 criterion |<T>/<V> + 0.5| < 0.2 over 20,000 ticks. Invariants.md now documents both standard (I4) and generalized (I4b) virial forms.
- [2026-10-07T11:15] agent-main: All Persian/Korean docs translated to English
- [2026-10-07T11:30] agent-main: Missing coordination files created
- [2026-10-10] agent-main: Test run: 8/9 under float32 (max relative energy drift 8.01e-08). x64 enabled per ADR-002 → 9/9 pass (CON-003 resolved). Opened CON-004 (undocumented 0.25 transverse-velocity constant in `_stabilized_state`; removing it breaks the virial test) — escalated to human, no code change.
- [2026-10-10] agent-main: CON-004 resolved via ADR-008 (rigid rotation about the mass centre, ω from the least-squares force balance). CON-005 resolved (G normalisation unified to 1/N). ADR-009: keep Python + JAX (measured ≈ 3.3M ticks/s; see docs/ToolSelection.md). 9/9 tests pass.
- [2026-10-10] agent-main: Status audit. `docs/prompt.md` was a stale truncated copy of ResearchLog.md → replaced with the agent entry prompt. TaskQueue.md T-003/T-004 moved to Completed. Changelog v0.2.0–v0.5.0 annotated as planned, not delivered (they named modules absent from the repo). Independently reproduced `pytest tests/ -v` → 9 passed (jax 0.10.2, pytest 9.1.1, Python 3.11).

## Blocked Tasks
- None unblocked by code, but note: T-005, T-006 and T-007 all depend on recorded L2 ticks and therefore await T-001/T-002 (Phase 1).
- Previously blocked, now resolved: CON-002 (log correction; generalized virial theorem documented in Physics.md for non-conservative systems), CON-003 (x64), CON-004 (ADR-008), CON-005 (G normalisation).

## Coordination Rules
1. Before starting a task, check this file and Conflicts.md
2. After completing a task, update this file with findings
3. If blocked, document in Conflicts.md and update this file
4. Every 10 tasks, consolidate knowledge and review

## Handoff
When handing off to another agent:
1. Update status to "Handed off to: [agent ID]"
2. Summarize current state in ResearchLog.md
3. List any blockers in Conflicts.md

## Latest Handoff (2026-10-10)

**Completed:** documentation status sync — prompt.md, TaskQueue.md, Changelog.md, AgentSync.md, ResearchLog.md.
**In Progress:** none.
**Blocked:** T-005/T-006/T-007 (await Phase 1 data ingestion).
**Next Priority:** T-001 — `fast_l2_client.py` WebSocket client (DataSpec.md), then T-002 — `tick_buffer` with Parquet storage.
**Notes:** repository code is unchanged and consistent; 9/9 tests pass. Open technical decisions: running time-average of ⟨d²⟩ (CON-005 remark) and the N ≥ 3 rigid-rotation residual (ADR-008).
