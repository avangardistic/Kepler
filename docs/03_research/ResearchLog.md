# Research Log

## [2025-01-15] [Phase 0] [Initialization]

**Goal:** Generate complete documentation structure.

**Method:** Generate 41 MD files via script.

**Result:** All files ready.

**Next:** Start T-001.

---

## [2026-10-07] [Phase 2] [physics_jax — Initial Implementation]

**Goal:** Implement three-body physics engine with symplectic integrator (velocity Verlet) in JAX.

**Method:**
- Create `ThreeBodyState` class with position, velocity, mass, imbalance, friction
- Define kinetic energy, potential energy, virial ratio, angular momentum functions
- Implement `symplectic_step` with equations of motion from Concept.md §3
- Implement `integrate` with `lax.scan` for long simulations
- Register ThreeBodyState as JAX pytree for JIT compatibility

**Result:**
- 9 unit tests passing: energy conserved (absolute drift < 1e-5), angular momentum bounded, virial ratio acceptable, imbalance always in [-1,1], zero-mass state frozen without NaN
- Bug fixes: kinetic energy formula, acceleration shape, JAX tracing with zero mass, initial state recording
- G_DEFAULT = 1e-6 for log-price position scale (later rejected — see Conflicts.md)

**Falsifications:**
- H2 virial test initially failed; later found to be a test design issue (see Conflicts.md CON-002)

**Next:**
- T-004: More invariant tests with varied scenarios
- T-001/T-002: WebSocket client and Parquet storage

---

## [2026-10-07] [Phase 0] [Documentation Migration]

**Goal:** Translate all Persian/Korean documentation to English, reject ADR-007, fix virial test.

**Method:**
- Full rewrite of ResearchLog.md, Decisions.md, Changelog.md to English
- Reject ADR-007 in Decisions.md (violates Axiom 4)
- Log G_DEFAULT violation in Conflicts.md as CON-001
- Update Physics.md with self-induced gravity formula
- Create missing coordination files (AgentSync.md, AgentHandoff.md, QA_Protocol.md, Paperclip_Coordination.md, Five_Whys_Template.md, FMEA_Template.md)

**Result:**
- All documentation now in English
- ADR-007 rejected, CON-001 logged
- Self-induced gravity formula documented in Physics.md
- Missing files created

**Next:**

---

## [2026-10-10] [Phase 2] [Verification, Precision Fix, and Documentation Correction]

**Goal:** Run the full test suite, fix failing configuration, and reconcile documentation with the actual test status.

**Method:**
- Installed `jax==0.10.2` and `pytest==9.1.1` in a virtualenv outside the repository and ran `pytest tests/ -v`.
- Baseline (default float32): 8 passed, 1 failed (`test_energy_conservation_relative_drift`, max relative drift 8.01e-08).
- Enabled x64 in `physics_jax.py` per ADR-002 (CON-003).
- Added `requirements.txt` (pins of the validated versions) and `.gitignore`; untracked committed `__pycache__/*.pyc` files.
- Experiment on a temporary copy only: removing the `0.25` transverse velocity injection breaks `test_virial_ratio_convergence` (CON-004).

**Result:**
- Default configuration: 9/9 tests pass, no environment variables required.
- The 2026-10-07 entry claiming "absolute drift < 1e-5" is incorrect; the I2 criterion is relative drift < 1e-9 (now met).
- Open: CON-004 (undocumented `0.25` constant, escalated to human).

**Falsifications:**
- Hypothesis "float32 is sufficient for I2 at 1e-9": falsified (drift 8.01e-08).

**Next:**
- Human decision on CON-004.
- T-001, T-002 (infrastructure), T-005 to T-007 remain open.

## [2026-10-10] [Phase 2] [Geometric Embedding (ADR-008) and Tool Selection (ADR-009)]

**Goal:** Remove the undocumented transverse-velocity constant (CON-004) using the most precise formula derivable from the documents, and decide whether any heavy computation needs another language.

**Method:**
- Tested candidate embeddings on copies in /tmp (not committed):
  - Same-direction velocity for all bodies: energy blows up (0.01 → 282); virial test fails.
  - Rigid rotation with Kepler speed and heuristic r̄: virial test passes (deviation 0.015).
  - Rigid rotation with least-squares ω from the force balance and Physics.md G (1/N): virial test passes (0.055 at 20k ticks, 0.0054 at 200k ticks).
- Found CON-005: the rotation used Physics.md G (1/N) while `integrate` used the code G (1/pairs). Inconsistent couplings gave ⟨T⟩/⟨V⟩ ≈ −2.39. Aligned both to one helper.
- Measured JAX throughput: ≈ 3.3 M ticks/s (3 bodies, float64, 2 CPU cores). 10 M ticks ≈ 3 s.
- 5 Whys analysis in docs/ToolSelection.md.

**Result:**
- Constant 0.25 removed; embedding derived from geometry (ADR-008, Physics.md §Embedding).
- All 9 tests pass in the default float64 configuration.
- Python + JAX kept; no other language introduced (ADR-009).
- Test comment about L ≈ 0 corrected (L ≈ 0.707 is a physical rotation); threshold unchanged.

**Falsifications:**
- Hypothesis "same-direction transverse velocity conserves energy": falsified (E: 0.01 → 282).
- Hypothesis "Python is too slow for 10 M ticks": falsified by measurement (≈ 3 s).

**Open:**
- Running time-average of G (Physics.md) is not implemented; initial-state G is used (CON-005 remark).
- N ≥ 3 rigid-rotation approximation residual not yet measured.
- T-001, T-002, T-005 to T-007 remain open.

---

## [2026-10-10] [Phase 2] [Status Audit and Documentation Sync]

**Goal:** Establish the actual project state from the repository (not from the
documents) and remove the inconsistencies found during the audit.

**Method:**
- Read `docs/prompt.md`, `docs/ResearchLog.md`, `docs/TaskQueue.md`,
  `docs/roadmap.md`, `docs/Changelog.md`, `docs/Conflicts.md`,
  `docs/AgentSync.md`, `README.md`, and `src/physics_jax.py`.
- Created a virtualenv outside the repository and installed the pinned
  versions (`jax==0.10.2`, `pytest==9.1.1`, Python 3.11) to reproduce the
  test run independently.

**Result — audited state:**
- `pytest tests/ -v` → **9 passed** (independently reproduced). The claim in
  README and in the 2026-10-10 entries is confirmed.
- Only source file is `src/physics_jax.py` (549 lines). No data ingestion,
  detectors, market-making or simulation code exists.
- Three documentation inconsistencies found and fixed:
  1. `docs/prompt.md` was a stale copy of `ResearchLog.md`, truncated at the
     2026-10-07 entry; replaced by a canonical agent entry prompt.
  2. `docs/TaskQueue.md` still listed T-003/T-004 as Open although both are
     complete in code and tests; moved to Completed, and T-005/T-006/T-007
     marked as blocked by T-001/T-002.
  3. `docs/Changelog.md` v0.2.0–v0.5.0 claimed `detectors_numba`,
     `market_maker`, `fast_l2_client` and `simulation_live_v3` were "added";
     none of them exists. Annotated as planned milestones.
- `docs/AgentSync.md` updated with the two 2026-10-10 sessions.

**Falsifications:**
- Hypothesis "the documents describe the state of the repository": falsified
  for `TaskQueue.md`, `Changelog.md` and `prompt.md`. Documentation drift is
  now corrected; the repository (code + tests) was already consistent.

**Next:**
- T-001 (fast_l2_client) and T-002 (tick_buffer / Parquet storage) are the
  highest-priority open tasks; every later phase needs recorded L2 ticks.
- Decide on the CON-005 open remark (running time-average of ⟨d²⟩) before
  Phase 5.
- Measure the N ≥ 3 rigid-rotation residual (ADR-008).

---

## [2026-10-11] [Phase 1] [Tick infrastructure delivered; real-data falsification of I2]

**Goal:** Execute the onboarding mission (`docs/MISSION_PROMPT.md`): clear the
blocking Phase 1 tasks T-001 (`fast_l2_client`) and T-002 (`tick_buffer` +
Parquet + replay), keep every invariant threshold untouched, and document the
state of the repository rather than the intent of its documents.

**Method:**
- **Documentation repair first.** Reconciled the docs with the repository and
  found that commit `829a846` had cyclically mis-filed six documents
  (`README.md`, `docs/prompt.md`, `TaskQueue.md`, `ResearchLog.md`,
  `Changelog.md`, `AgentSync.md`): each file held the content of its neighbour
  (e.g. `TaskQueue.md` held the research log). Contents were restored from the
  working tree and `README.md` was taken from the newer `829a846^` revision;
  logged as CON-006. Re-verified the baseline in a fresh venv: 9 passed.
- **T-001** `src/fast_l2_client.py`: raw `depth20@100ms` snapshot client for
  btcusdt/ethusdt/solusdt. Pull-based streaming (a slow consumer pauses the
  reader, so nothing can be dropped), optional uvloop/orjson with stdlib
  fallbacks (ADR-010), per-symbol sequence-regression counter, DataSpec
  book validation *counted but never enforced* (no filtering), and a CLI
  (`python -m src.fast_l2_client`).
- **T-002** `src/tick_buffer.py`: bounded `TickBuffer` → `L2ParquetStore`
  (Parquet/zstd, `symbol=<S>/day=<YYYY-MM-DD>/part-NNNN.parquet`) and
  `TickReplay` (`ticks()`, `states()` → `state_from_l2`). Strict ordering is
  enforced (`TickOrderError`), and a dependency-free Parquet footer reader
  (`parquet_codecs`) verifies the zstd requirement instead of inferring it.
  ADR-011 records the feed/storage decisions (snapshots not diffs, latest-wins
  alignment, no derived quantities stored).
- **Tests** (offline, deterministic, injected clock and transport):
  `tests/test_fast_l2_client.py` (17) and `tests/test_tick_buffer.py` (13) —
  including a real loopback WebSocket run and the 100 000-tick acceptance run.
- **Live run.** `stream.binance.com` answered **HTTP 451** from this network;
  `data-stream.binance.vision` served the identical payloads. Captured 2 785
  live ticks in 120 s to Parquet and replayed them through the physics path.
- **Measurements** (this sandbox, Python 3.11, Windows, 2 cores): client
  12 872 ticks/s end-to-end over loopback (20 levels/side); store write
  6 837 ticks/s; replay 24 244 ticks/s; 26.6 bytes/tick; and
  `TickReplay.states()` (one `state_from_l2` call per tick) 76 states/s,
  i.e. **13.1 ms per state** — ~2 600x slower than the integrator (3.3 M
  ticks/s, ADR-009). Any Phase 3-5 loop that needs a state per tick must
  jit/vmap the state construction; recycling the replay generator as-is would
  cap a 10 M-tick run at ~36 hours.

**Result:**
- `pytest tests/ -v` → **41 passed** (9 physics + 17 client + 15 storage) with
  the pinned requirements (`jax 0.10.2`, `pytest 9.1.1`, `websockets 17.2`,
  `orjson 3.13.0`, `polars 2.0.0`). The nine pre-existing physics tests are
  untouched and still pass; no threshold was modified.
- Acceptance (T-001 criterion): 100 000 ticks, `dropped == 0`,
  `out_of_order == 0`, `invalid_books == 0` (offline, in-process source), plus
  a real loopback WebSocket run and a 2 785-tick live capture with 0 invalid
  books and 20 levels on every tick.
- Deterministic replay verified: repeated `TickReplay` on one dataset yields
  identical ticks and an identical `integrate` trajectory.
- Documentation updated: ADR-010, ADR-011, CON-006, CON-007, DataSpec, Invariants
  (Phase 1 guarantees), Implementation, roadmap, TaskQueue, Changelog, README.
- Environment note: this CPU lacks AVX2/FMA/BMI, so the default `polars` runtime
  refuses to run; `polars[rtcompat]==2.0.0` is used and pinned.

**Falsifications:**
- Hypothesis "`stream.binance.com` can be used from this network": falsified
  (HTTP 451). Alternative domain verified live instead (CON-007).
- Hypothesis "the documents describe the repository": falsified again for six
  files (CON-006), the second occurrence of this class of drift.
- **Hypothesis "the physics invariants hold on real L2 data at dt = 1 tick":
  FALSIFIED.** Replaying the live capture and integrating 2 000 ticks:

  | Path | ‖L‖₀ | ‖L‖ₘₐₓ | E₀ | max relative energy drift |
  |---|---|---|---|---|
  | 2-D `state_from_l2`, conservative | 0 | 0 | −1.008 | 281 |
  | 2-D `state_from_l2`, with imbalance + friction | 0 | 6.25e4 | −1.008 | 6.2e6 |
  | 1-D ⇒ ADR-008 embedding, conservative | 8.484 | 8.484 | −0.6255 | 1.54 |
  | 1-D ⇒ ADR-008 embedding, with imbalance + friction | 8.484 | 1.65e6 | −0.6255 | 1e7 |

  I2 requires < 1e-9. Two causes identified: (a) `state_from_l2` returns a
  2-D state, so `_stabilized_state` never applies the ADR-008 rigid-rotation
  embedding to L2-built states; (b) the scalar imbalance is added to *every*
  acceleration component, which injects angular momentum. Recorded as F10 in
  FailureModes.md and CON-008 in Conflicts.md (open, escalated).
- Hypothesis "plain `polars` works everywhere": falsified on this CPU (missing
  AVX2); `polars[rtcompat]` required.

**Next:**
- **CON-008 decision (highest priority).** Four candidate directions are listed
  in Conflicts.md; each requires an ADR and a re-measurement on the captured
  dataset. Until then, Phase 5 (`Π > 0`) cannot be run honestly.
- T-005 `detectors_numba.py` (F1 > 0.8 on synthetic data) — it consumes recorded
  ticks and does not call `integrate`, so it is unblocked by CON-008.
- jit/vmap the replay→state path: `TickReplay.states()` costs 13.1 ms per
  tick (76 states/s, measured 2026-10-11) because it calls `state_from_l2`
  outside any jit. Phase 3-5 loops need per-tick states.
- Complete the full live acceptance run (~55 min at the observed ~23 ticks/s):
  `python -m src.fast_l2_client --ticks 100000 --out data/l2`.
- The live 2,785-tick capture is now committed as `tests/data/live_2026-10-11/` with provenance notes; the earlier statement that it existed only in a temporary directory is superseded. It remains a small fixture, not a full 100,000-tick live run.

---

## [2026-10-11] [Documentation] [Category migration and workflow rewrite]

**Goal:** Execute the planned documentation categorization in one pass, remove stale agent instructions, and make project status and research boundaries match the code and recorded evidence.

**Changes:**
- Moved the 48 canonical topic documents into five functional categories: theory (16), engineering (7), research (13), planning/workflow (9), and reference (3). Added flat compatibility stubs for old paths; `docs/README.md` is the canonical index, while `docs/INDEX.md` and `docs/prompt.md` now point to the index and current onboarding prompt. Updated the committed fixture README to use canonical research paths.
- Added `AGENTS.md` and rewrote the mission prompt, reusable prompts, AI protocol, QA protocol, handoff process, manual sync, and optional external-coordination guidance using a concise objective → inspect → change → verify → report loop.
- Reconciled stale current-state text: Phase 1/T-001/T-002 exist; the last recorded suite is 41 tests; real-data I1/I2 still fail under CON-008; T-005 is open and unblocked; T-006 is blocked by a scope conflict; Phase 5 is not validated.
- Corrected the unsupported statement that risk is “solved by geometry” (CON-010, documentation clarification) and recorded the market-making/quote-generation mismatch as CON-009 (open). No code or acceptance threshold changed.

**Verification:**
- Markdown link audit: 104 Markdown files scanned, 0 broken relative targets.
- Category inventory: 48 canonical docs accounted for (16 + 7 + 13 + 9 + 3); 48 flat compatibility stubs retained.
- `git diff --check`: passed.
- Python tests: `python -m pytest -q` could not start (`/usr/bin/python: No module named pytest`); JAX and the Phase 1 runtime dependencies are also absent. The historical 41-pass result is not represented as a current run.

**Outcome:** documentation-only change. CON-008 and CON-009 remain open; no model resolution was invented.
