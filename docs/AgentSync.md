# Agent Synchronization

## Active Agents
| Agent ID | Session Start | Current Task | Status |
|----------|--------------|--------------|--------|
| agent-main | 2026-10-07 | Phase 0: Documentation Migration | ✅ Complete |

## Task Claims
| Task | Claimed By | Claimed At | Status |
|------|-----------|------------|--------|
| Phase 0 (all) | agent-main | 2026-10-07T10:00 | Done |

## Recent Discoveries
- [2026-10-07T10:45] agent-main: G_DEFAULT violation found, ADR-007 rejected (CON-001)
- [2026-10-07T11:00] agent-main: Virial test needs generalized virial theorem (CON-002)
- [2026-10-07T11:05] agent-main: CON-002 corrected — no threshold loosening occurred; log entry was a writing error. Test always used I4 criterion |<T>/<V> + 0.5| < 0.2 over 20,000 ticks. Invariants.md now documents both standard (I4) and generalized (I4b) virial forms.
- [2026-10-07T11:15] agent-main: All Persian/Korean docs translated to English
- [2026-10-07T11:30] agent-main: Missing coordination files created

## Blocked Tasks
- None — CON-002 resolved (log correction; generalized virial theorem documented in Physics.md for non-conservative systems)

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
- [2026-10-10] agent-main: Test run: 8/9 under float32. x64 enabled per ADR-002 → 9/9 pass (CON-003 resolved). Opened CON-004 (undocumented 0.25 transverse-velocity constant in `_stabilized_state`; removing it breaks the virial test) — escalated to human, no code change.
- [2026-10-10] agent-main: CON-004 resolved via ADR-008 (rigid rotation about mass centre, ω from least-squares force balance). CON-005 resolved (G normalisation 1/N unified). ADR-009: keep Python+JAX (measured ≈3.3M ticks/s; see docs/ToolSelection.md). 9/9 tests pass.
