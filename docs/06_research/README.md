# Research Topics — Active

Only active research lives here. Solved/closed topics move to `11_meta/`
(with a pointer left in this README). IDs are permanent: `R-<AREA>-<###>`.

## Physics Research

### [R-PHY-001] Virial Theorem for Non-Conservative Systems
- **Status:** ✅ RESOLVED (Session 2, 2026-10-07)
- **File:** `physics/virial_theorem.md`
- **Question:** Does T/V converge to −0.5? If not, what is the correct value?
- **Answer:** −0.5 holds instantaneously only for circular orbits (≥2-D) and
  as a time-average over exact integer periods for any eccentricity
  (verified to ~1e-9). The old "−1.0" was (a) a 1-D radial-plunge setup with
  numerical heating and (b) a test assignment bug. CON-002 closed.
- **Follow-ups extracted:** R-PHY-003 (resolution conditions), F10.

### [R-PHY-002] Self-Induced Gravity Derivation
- **Status:** OPEN
- **File:** `physics/gravity_derivation.md`
- **Question:** Is G_eff = 1/⟨d²⟩_t correct? Running-average vs frozen-initial
  divergence between Physics.md and `integrate()` — which satisfies Axiom 4?
- **Key constraint found:** energy conservation (I2) and the standard virial
  theorem require constant G; circular orbits are the only Kepler family
  where instantaneous and frozen G coincide.
- **Owner:** [unassigned]

### [R-PHY-003] Orbital Stability Conditions
- **Status:** PARTIAL — resolution criteria derived + measured, formal experiment pending
- **File:** `physics/orbital_conditions.md`
- **Question:** What initial conditions produce bounded ‖L‖ and numerically
  resolvable dynamics?
- **Owner:** [unassigned]

### [R-PHY-004] Generalized Virial Theorem
- **Status:** DERIVED, awaiting test implementation
- **File:** `physics/generalized_virial.md`
- **Question:** How do F_ext = I·m and friction −γ·v enter the virial?
- **Deliverable to close:** a test asserting the four-term identity with
  I≠0, γ≠0 (proposed as T-008 in `12_prompts/TaskQueue.md`).

## Detector Research

### [R-DET-001] Iceberg Detection Math
- **Status:** NOT STARTED (framing sketch in file)
- **File:** `detectors/iceberg_math.md`
- **Constraint:** detection must emerge from geometry (mass/force), no
  filters or indicators (Philosophy §2).

### [R-DET-002] Spoof Detection Math
- **Status:** NOT STARTED (framing sketch in file)
- **File:** `detectors/spoof_math.md`

## Market Making Research

### [R-MM-001] Avellaneda-Stoikov to Three-Body Mapping
- **Status:** DRAFT
- **File:** `market_making/avellaneda_stoikov_mapping.md`
- **Core tension:** A-S consumes exogenous (σ, γ, T−t); Kepler forbids
  external parameters. Mapping must be self-consistent or it is a falsification.

## General Open Problems (inherited, 10 items)
→ `open_problems.md` (was `docs/OpenProblems.md`; still Persian, translate when touched)

## How to Add a New Research Topic
1. Create a file in the appropriate subfolder of `06_research/`.
2. Add an entry here with a new `R-XXX-###` ID, status, question, owner.
3. Link from `07_hypotheses/Hypotheses.md` if the topic yields a testable claim.
4. Update `docs/00_INDEX.md` "Current Status" if it changes the headline state.
5. When resolved: keep the file (it is the record), flip status to ✅ RESOLVED,
   and reference the code/test that closes it.
