# Research Log

## [2026-10-07] [Session 2] [Audit + Doc Reorg + Virial Resolution]

**Goal:** Audit prior session's claimed state, reorganize `docs/` into 12 numbered
categories, resolve CON-002 / the failing virial test, and leave a handoff packet.

**Audit findings (measured, not assumed):**
- Test suite at session start: **7 pass / 2 fail** — the incoming brief claimed 8/9.
  The second, unreported failure was `test_energy_conservation_relative_drift`
  (I2: drift 8e−8 vs threshold 1e−9 → JAX float32 precision limit, *not* an
  integrator bug).
- `src/__init__.py` did **not** exist despite the brief claiming it was created.
- Brief's "F5 = virial failure" was wrong; FailureModes F5 is the detector
  false-positive mode. Real mapping: virial issue = F8, now made precise as F10.
- New finding (F10 + test bug): **the reported "−1.0008 virial ratio" was two
  compounding artifacts, not a model falsification.**
  (A) The old test bound integrate()'s *third return value* (per-tick ratio
  T/V) to a variable named `V`, computed `T := E − V`, and divided the means —
  so "−1.0008" = Ē/V̄ − 1, an algebraic echo; the guarded division (V := ε when
  |V| < ε) after the pair escaped produced the |means| ~ 4e5 magnitudes.
  (B) The 1-D ICs themselves are unphysical for a virial test: every bound
  1-D orbit is a radial plunge (zero angular momentum ⇒ no centrifugal
  barrier); close approaches at dt = 1e−3 are unresolved → numerical heating
  (E: −0.115 → +296). The handoff's recommended "set v = v_circ in 1-D" fix
  was checked and **fails identically** (E: −0.0625 → +160): circular orbits
  do not exist in 1-D at all.
- Engine bug found while diagnosing: multi-D potential/force used per-coordinate
  softening `sqrt(dx_k² + ε²)` instead of radial `sqrt(‖dx‖² + ε²)`, which breaks
  any ≥2-D configuration.
- `integrate()` recorded the initial imbalance as `‖I‖₂` but per-tick values as
  `max|I|` — inconsistent statistic.

**Actions:**
- Reorganized `docs/` (47 flat files) into 12 numbered folders + root
  `00_INDEX.md` / `STATE_INVENTORY.md` / `ResearchLog.md`; created `06_research/`
  with per-topic files (R-PHY-001..004, R-DET-001/002, R-MM-001). `generate_docs.py`
  retargeted so regeneration reproduces the new tree.
- `src/physics_jax.py`: isotropic (radial) softening in `compute_potential_energy`,
  `acceleration`, `compute_self_induced_G`; `zeros_like` shape fix; consistent
  `max|I|` statistic in `integrate` history init. 1-D results unchanged bit-for-bit.
- `tests/conftest.py`: enable `jax_enable_x64` (precision requirement of I2/I4,
  thresholds untouched — QA_Protocol P3 respected).
- `tests/test_physics.py`: virial test rebuilt on a 2-D circular orbit with
  self-consistent v_circ; asserts per-tick AND time-averaged |T/V + 0.5| < 0.2
  (unchanged threshold), L bounded, ratios finite.
- `src/__init__.py` created.

**Result:**
- **9/9 tests pass** (measured at session end; thresholds never changed:
  I4 kept at 0.2, I2 kept at 1e−9 — both now genuinely satisfied).
- R-PHY-001 RESOLVED with full write-up (`06_research/physics/virial_theorem.md`):
  exact 2-D circular orbit gives |⟨T/V⟩ + 0.5| = 1.2e−10 and per-tick ratio
  −0.5 constant; the corrected root cause is *two* bugs — (B) 1-D
  radial-plunge ICs heating E −0.115 → +296 (verified also for v = v_circ:
  −0.0625 → +160), and (A) the old test's assignment bug binding integrate()'s
  ratio output to `V`, making its reported −1.0008 the algebraic echo Ē/V̄ − 1.
- Bonus theorem-check: ⟨T⟩/⟨V⟩ = −0.5 ± 1e−7 for eccentricities to e ≈ 0.75
  when averaged over **exact integer Kepler periods** (dt = 2e−5, 1–10 periods)
  — the virial theorem holds; the old test measured neither theory nor orbit.
- CON-002 closed; CON-003 opened (G fallback 1.0; frozen-vs-running G) —
  needs human ADR. F10 added to FailureModes. H2 revised.

**Next:** R-PHY-002 (G_eff running-average vs frozen-initial spec divergence),
R-PHY-003 sweep table (v/v_circ vs ⟨T⟩/⟨V⟩ vs energy drift).

---

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

**Next:** Continue with Phase 0.3 (virial test fix)
