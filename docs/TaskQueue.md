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
