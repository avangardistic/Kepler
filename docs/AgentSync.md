# Agent Synchronization

## Active Agents
| Agent ID | Session Start | Current Task | Status |
|----------|--------------|--------------|--------|
| agent-main | 2026-10-07 | Phase 0: Documentation Migration | ✅ Complete |
| agent-main | 2026-10-10 | Phase 2: Verification and precision fix | ✅ Complete |
| agent-main | 2026-10-10 | Phase 2: Geometric embedding (ADR-008), tool decision (ADR-009) | ✅ Complete |
| agent-main | 2026-10-10 | Status audit and documentation sync (no code change) | ✅ Complete |
| agent-main | 2026-10-11 | Phase 1: T-001 fast_l2_client, T-002 tick_buffer/Parquet/replay; docs repair (CON-006) | ✅ Complete |

## Task Claims
| Task | Claimed By | Claimed At | Status |
|------|-----------|------------|--------|
| Phase 0 (all) | agent-main | 2026-10-07T10:00 | Done |
| T-003 (physics_jax) | agent-main | 2026-10-07 | Done — recorded in TaskQueue.md 2026-10-10 |
| T-004 (invariant tests) | agent-main | 2026-10-07 | Done — recorded in TaskQueue.md 2026-10-10 |
| T-001 (fast_l2_client) | agent-main | 2026-10-11 | Done — `src/fast_l2_client.py`, 15 tests, 100k-tick offline acceptance, live smoke run |
| T-002 (tick_buffer/Parquet/replay) | agent-main | 2026-10-11 | Done — `src/tick_buffer.py`, 13 tests, deterministic replay verified |
| T-001, T-002 | — | — | Claimed and completed 2026-10-11 |

## Recent Discoveries
- [2026-10-07T10:45] agent-main: G_DEFAULT violation found, ADR-007 rejected (CON-001)
- [2026-10-07T11:00] agent-main: Virial test needs generalized virial theorem (CON-002)
- [2026-10-07T11:05] agent-main: CON-002 corrected — no threshold loosening occurred; log entry was a writing error. Test always used I4 criterion |<T>/<V> + 0.5| < 0.2 over 20,000 ticks. Invariants.md now documents both standard (I4) and generalized (I4b) virial forms.
- [2026-10-07T11:15] agent-main: All Persian/Korean docs translated to English
- [2026-10-07T11:30] agent-main: Missing coordination files created
- [2026-10-10] agent-main: Test run: 8/9 under float32 (max relative energy drift 8.01e-08). x64 enabled per ADR-002 → 9/9 pass (CON-003 resolved). Opened CON-004 (undocumented 0.25 transverse-velocity constant in `_stabilized_state`; removing it breaks the virial test) — escalated to human, no code change.
- [2026-10-10] agent-main: CON-004 resolved via ADR-008 (rigid rotation about the mass centre, ω from the least-squares force balance). CON-005 resolved (G normalisation unified to 1/N). ADR-009: keep Python + JAX (measured ≈ 3.3M ticks/s; see docs/ToolSelection.md). 9/9 tests pass.
- [2026-10-10] agent-main: Status audit. `docs/prompt.md` was a stale truncated copy of ResearchLog.md → replaced with the agent entry prompt. TaskQueue.md T-003/T-004 moved to Completed. Changelog v0.2.0–v0.5.0 annotated as planned, not delivered (they named modules absent from the repo). Independently reproduced `pytest tests/ -v` → 9 passed (jax 0.10.2, pytest 9.1.1, Python 3.11).

- [2026-10-11] agent-main: Documentation repair. Commit `829a846` had cyclically mis-filed six docs (README/prompt/TaskQueue/ResearchLog/Changelog/AgentSync). Contents restored to their canonical paths; logged as CON-006. Root cause: a rename/copy script that shifted filenames; no code impact.
- [2026-10-11] agent-main: T-001 delivered (`src/fast_l2_client.py`). 100 000-tick offline acceptance: `dropped == 0`, `out_of_order == 0`, `invalid_books == 0`; 17 tests pass. Measured end-to-end throughput over a loopback WebSocket: 12 872 ticks/s (20 levels/side, 60 000 messages) — ≈ 430× the live feed rate of 3 assets × 10 ticks/s.
- [2026-10-11] agent-main: T-002 delivered (`src/tick_buffer.py`). Parquet/zstd, `symbol/day/part-NNNN`, strict `tick_index` ordering, deterministic replay into `state_from_l2`/`integrate`; 13 tests pass. Measured: write 6 837 ticks/s, replay 24 244 ticks/s, 26.6 B/tick (10 M ticks ≈ 0.27 GB, below the 1 GB DataSpec estimate).
- [2026-10-11] agent-main: Live capture. `stream.binance.com` answers **HTTP 451** from this network; `data-stream.binance.vision` serves the identical streams. Captured 2 785 live ticks in 120 s (BTCUSDT 1 165 / ETHUSDT 1 151 / SOLUSDT 469; 20 levels per side; 0 invalid books). Endpoint choice documented in ADR-011 + CON-007.
- [2026-10-11] agent-main: Replay→state cost measured: `TickReplay.states()` 76 states/s (13.1 ms per tick) because `state_from_l2` is not jitted — ~2 600× slower than the integrator. Recorded in TaskQueue/ResearchLog as a Phase 3–5 prerequisite.
- [2026-10-11] agent-main: The 2 785-tick live capture is now committed as a repo fixture (`tests/data/live_2026-10-11`, 72 KB, with a provenance README) so CON-008 stays reproducible offline. Its tests assert retention guarantees only — never that the invariants hold.
- [2026-10-11] agent-main: **CON-008 opened from real data.** Replaying the live capture at `dt = 1` tick, I2 fails badly (max relative energy drift 281 conservative, 1.54 with the ADR-008 embedding, up to 6.2e6 with imbalance) and the ADR-008 embedding is bypassed for L2-built states because `state_from_l2` returns a 2-D state. Measured table in FailureModes.md F10. No threshold was loosened; 41/41 tests still pass because they use purpose-built configurations.

## Blocked Tasks
- **CON-008 (open, escalated to human):** all real-data invariant work. Phase 3 detectors can proceed on recorded ticks (they do not use `integrate`), but Phase 5 (`Π > 0`) is blocked until a model decision is recorded as an ADR.
- T-005 no longer awaits T-001/T-002: recorded ticks now exist (`TickReplay` + `L2ParquetStore`).
- Previously blocked, now resolved: CON-002 (log correction; generalized virial theorem documented in Physics.md for non-conservative systems), CON-003 (x64), CON-004 (ADR-008), CON-005 (G normalisation, one open remark), CON-006 (docs re-filed), CON-007 (`ts_exchange` semantics).

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

## Latest Handoff (2026-10-11)

**Completed:** Phase 1 (T-001 `src/fast_l2_client.py`, T-002 `src/tick_buffer.py`), 32 new tests, ADR-010/ADR-011, CON-006/CON-007 resolved, a 120 s live capture, and the real-data falsification recorded as F10/CON-008.
**In Progress:** none.
**Blocked:** CON-008 — needs a human decision on the real-data I1/I2 failure (candidates in Conflicts.md) before Phase 5. The full 100 000-tick *live* acceptance run (~55 min at ~30 ticks/s) has not been performed; the offline 100 000-tick run has.
**Next Priority:** (1) CON-008 decision; (2) T-005 `detectors_numba.py` (F1 > 0.8 on synthetic data) — recorded ticks are now available; (3) complete the live 100k run with `python -m src.fast_l2_client --ticks 100000`.
**Notes:** 41/41 tests pass in the validated environment (Python 3.11, jax 0.10.2, pytest 9.1.1, polars 2.0.0 with the `rtcompat` runtime — the CPU here has no AVX2, so plain `polars` crashes; see CON-006-adjacent note in DataSpec/ADR-011). Open technical decisions: CON-005 running time-average of ⟨d²⟩, CON-008, and the newly measured N ≥ 3 embedding residual.
