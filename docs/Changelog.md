# Changelog

> **Accuracy note (2026-10-10).** The v0.2.0–v0.5.0 entries below were produced
> by the initial documentation generator and describe work that is **not
> present in this repository**. As of 2026-10-10 the only source file is
> `src/physics_jax.py`; `fast_l2_client`, `tick_buffer`, `detectors_numba`,
> `market_maker` and `simulation_live_v3` do not exist. They are recorded here
> as planned milestones (roadmap Phase 1, 3, 4, 5), not delivered features.

## v0.1.0 — 2025-01
- Initial Concept, Philosophy, Strategy.

## v0.2.0 — 2025-01 (planned — not in repository)
- Added Implementation (documentation: `docs/Implementation.md`).
- Introduced physics_jax (delivered later, 2026-10-07).

## v0.3.0 — 2025-01 (planned — not in repository)
- Added detectors_numba. → roadmap Phase 3, task T-005.
- Added market_maker (A-S). → roadmap Phase 4, task T-006.

## v0.4.0 — 2025-01 (planned — not in repository)
- Migrated to uvloop + orjson. → roadmap Phase 1.
- Added fast_l2_client. → roadmap Phase 1, task T-001.

## v0.5.0 — 2025-01 (planned — not in repository)
- Ten L2 states.
- simulation_live_v3. → roadmap Phase 5, task T-007.

## v1.0.0 — (target)
- 10 million ticks.
- Full validation.
- Whitepaper.

## [2026-10-07] — physics_jax.py
- Implemented `symplectic_step` (velocity Verlet)
- Implemented `integrate` with lax.scan
- JAX pytree registration for ThreeBodyState
- Invariant tests: energy, angular momentum, virial, imbalance
- Zero-mass (empty book) support without NaN

## [2026-10-07] — Documentation Migration
- Translated all Persian/Korean documentation to English
- Rejected ADR-007 (G_DEFAULT violates Axiom 4)
- Added self-induced gravity formula to Physics.md
- Created coordination files (AgentSync, AgentHandoff, QA_Protocol, etc.)
- Corrected CON-002 log entry (prior pass mistakenly recorded a threshold loosening
  that never occurred; the test always used the I4 criterion |<T>/<V> + 0.5| < 0.2)

## [2026-10-10] — Verification and Precision Fix
- Enabled x64 precision in physics_jax.py (ADR-002); energy test (I2, 1e-9) now passes on default configuration. All 9 tests pass.
- Added requirements.txt (jax 0.10.2, pytest 9.1.1).
- Added .gitignore; untracked committed __pycache__ bytecode files.
- Correction: the 2026-10-07 log claim of "absolute drift < 1e-5" did not match the I2 criterion (relative 1e-9). See Conflicts.md CON-003.
- Opened CON-004: undocumented transverse velocity constant (0.25) in `_stabilized_state`, escalated for decision.

## [2026-10-10] — Geometric Embedding and Tool Decision
- Replaced undocumented `0.25·sign(v)` with rigid-rotation embedding derived from self-induced gravity (ADR-008, CON-004 resolved).
- Unified self-induced G to Physics.md normalisation (1/N) in one helper (CON-005 resolved).
- Corrected the virial-test comment on angular momentum; threshold unchanged.
- Added docs/ToolSelection.md (5 Whys, measured throughput) and ADR-009: keep Python + JAX.
- All 9 tests pass in default configuration.

## [2026-10-10] — Documentation Status Sync (no code change)
- `docs/prompt.md`: replaced a stale, truncated copy of `ResearchLog.md`
  (stopped at 2026-10-07) with the canonical agent entry prompt.
- `docs/TaskQueue.md`: T-003 and T-004 moved to Completed with verification
  evidence; T-005/T-006/T-007 marked blocked by T-001/T-002; follow-ups listed.
- `docs/Changelog.md`: v0.2.0–v0.5.0 annotated as planned, not delivered —
  they described modules absent from the repository.
- `docs/AgentSync.md`: recorded the two 2026-10-10 sessions.
- Verified after the sync: `pytest tests/ -v` → 9 passed (jax 0.10.2,
  pytest 9.1.1, Python 3.11).

## [2026-10-11] — Phase 1 delivered: raw L2 client, Parquet storage, replay
- **New:** `src/fast_l2_client.py` (T-001) — raw `depth20@100ms` snapshot client
  for BTC/ETH/SOL, pull-based and drop-free, optional uvloop/orjson (ADR-010),
  per-symbol sequence checks, DataSpec validation counted but not enforced, and
  a capture CLI: `python -m src.fast_l2_client --ticks 100000 --out data/l2`.
- **New:** `src/tick_buffer.py` (T-002) — bounded `TickBuffer`, `L2ParquetStore`
  (Parquet + zstd, `symbol=<S>/day=<YYYY-MM-DD>/part-NNNN.parquet`), strict
  `tick_index` ordering, deterministic `TickReplay` into `state_from_l2`, and
  `parquet_codecs()` for dependency-free verification of the zstd requirement
  (ADR-011).
- **Tests:** +32, all offline and deterministic — `tests/test_fast_l2_client.py`
  (17) and `tests/test_tick_buffer.py` (15). `pytest tests/ -v` → **41 passed**
  (9 physics + 32 new). No existing test or threshold was changed.
- **Acceptance:** 100 000 ticks with `dropped == 0` and `out_of_order == 0`
  (T-001 exit criterion), plus a loopback WebSocket run and a 2 785-tick live
  capture on 2026-10-11.
- **Decisions:** ADR-010 (uvloop/orjson are optional: uvloop is POSIX-only),
  ADR-011 (snapshot feed, Parquet/zstd layout, latest-wins replay alignment).
- **Conflicts:** CON-006 resolved (six docs cyclically mis-filed by commit
  `829a846` — contents restored to canonical paths), CON-007 resolved
  (`ts_exchange_ns == 0` for streams without an exchange timestamp),
  **CON-008 opened** (I1/I2 fail on real L2 replay at `dt = 1`; see F10).
- **Docs:** DataSpec (schema, layout, codec, validation semantics), Invariants
  (Phase 1 guarantees table), Implementation (actual stack and folder layout,
  implemented vs planned tick flow), roadmap (Phase 1 status), TaskQueue,
  AgentSync, ResearchLog, FailureModes F6/F10, README.
- **Dependencies:** `requirements.txt` gained `websockets==17.2`,
  `orjson==3.13.0`, `polars==2.0.0` (installed as `polars[rtcompat]`: this CPU
  has no AVX2, and the default polars runtime refuses to run without it).
- **Note:** the physics engine is unchanged. CON-008 means the real-data
  invariant results are currently negative and must not be reported as passes.
