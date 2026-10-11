# Changelog

> **Accuracy note (updated 2026-10-11).** The v0.2.0–v0.5.0 entries below were
> produced by the initial documentation generator. At the time the note was
> first written (2026-10-10) the only source file was `src/physics_jax.py`.
> Since then `src/fast_l2_client.py` (T-001) and `src/tick_buffer.py` (T-002)
> were delivered on 2026-10-11 under the *latest* entries below, and the
> Implementation documentation exists. `detectors_numba`, `market_maker` and
> `simulation_live_v3` are still **not** present and remain planned milestones
> (roadmap Phases 3, 4, 5).

## v0.1.0 — 2025-01
- Initial Concept, Philosophy, Strategy.

## v0.2.0 — 2025-01 (partly delivered)
- Added Implementation documentation (the document exists; see `docs/02_engineering/Implementation.md`).
- Introduced physics_jax (delivered later, 2026-10-07).

## v0.3.0 — 2025-01 (planned — not in repository)
- Added detectors_numba. → roadmap Phase 3, task T-005.
- Added market_maker (A-S). → roadmap Phase 4, task T-006.

## v0.4.0 — 2025-01 (delivered 2026-10-11)
- uvloop + orjson used where available with stdlib fallbacks. → ADR-010.
- `fast_l2_client` delivered as `src/fast_l2_client.py`. → T-001, 2026-10-11.

## v0.5.0 — 2025-01 (planned — not in repository)
- Ten L2 states (draft taxonomy documented in `docs/03_research/RegimeCatalog.md`; no classifier implemented).
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

## [2026-10-11] — Documentation & hygiene (audit)

- **New at the time:** `docs/README.md` navigation hub + `docs/INDEX.md` alias — categorised index of all 48 docs with suggested reading orders. The planned `01_theory … 05_reference` move was deferred at this audit; it was completed in the later 2026-10-11 documentation architecture refresh below.
- **New:** `CHANGES_TEMPLATE.md` (repo root) — standard change-report format with policy-alignment checklist per `docs/QA_Protocol.md` and `docs/Invariants.md` (audit §3).
- **New:** `CONTRIBUTING.md` — contributor workflow, per-change checklist, project structure and escalation path.
- **Code hygiene:** `src/fast_l2_client.py` `__all__` policy clarified (internal `_loads`, `_levels`, `_websockets_connector` intentionally excluded); `src/physics_jax.py` `state_from_l2` now emits `logger.debug` on empty-book / zero-depth edge cases (self-freeze F2) instead of silently returning `0.0` (audit §1.1/§1.2).
- **Docs:** `README.md` repository layout and documentation section updated to point to `docs/README.md` hub and `CHANGES_TEMPLATE.md`.
- **Policy:** no invariant threshold changed, no external parameter added, no file moved — `pytest tests/ -v` still **41/41**. See `CHANGES_TEMPLATE.md §3` for the alignment checklist used.

## [2026-10-11] — Documentation architecture and workflow refresh

- **Organization:** moved all 48 canonical topic documents into `01_theory/`, `02_engineering/`, `03_research/`, `04_planning/`, and `05_reference/`. Kept flat compatibility stubs and replaced duplicate `INDEX.md` / stale `prompt.md` content with pointers to canonical entry points; updated the committed-fixture README to cite canonical research paths.
- **Prompts/workflow:** added root `AGENTS.md`; rewrote the mission prompt, reusable prompt library, AI protocol, QA workflow, handoff, manual sync, and optional Paperclip guidance around a small evidence-led task loop.
- **Status repair:** updated goals, roadmap, task queue, README, and contributor docs to match implemented Phase 1/2 code and the open CON-008 real-data failure; T-005 is unblocked, T-006 needs a scope decision, and Phase 5 remains blocked.
- **Scientific clarity:** replaced the unsupported “risk solved by geometry” claim with an explicit scope-only statement (CON-010 resolved as documentation); recorded the quote-generation/anti-goal mismatch as CON-009 open. No code, test threshold, or invariant was changed.
- **Validation:** internal Markdown link/anchor audit scanned 104 Markdown files and found 0 broken targets; category inventory is 48/48. `git diff --check` passed. `python -m pytest -q` could not start (`No module named pytest`); JAX and the Phase 1 runtime dependencies are also absent, so the test suite was not run.
