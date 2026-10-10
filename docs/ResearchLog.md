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
