# Kepler State Inventory

> Living file. Every agent reads this BEFORE acting and updates it AFTER acting.
> Pair with `09_agents/AgentSync.md`. Do not trust session prompts or chat
> memory — trust this file and the tests.

## Last Updated: 2026-10-07 (Session 2, end-of-session state)

## Test Status (measured at session end, `python -m pytest tests/ -v`)
- Total: 9 · **Passing: 9** · Failing: 0 · Skipped: 0
- Thresholds are exactly those of `07_hypotheses/Invariants.md` (I4: 0.2,
  I2: 1e−9) — never loosened (QA_Protocol P3). float64 via `tests/conftest.py`
  is a *precision requirement*, documented there.
- At Session-2 start the measured state was **7/9** (the incoming brief's
  "8/9" was wrong; the extra failure was the float32-limited I2 test).

## Files
| Path | Status | Purpose | Note |
|------|--------|---------|------|
| `src/physics_jax.py` | active | Physics engine (velocity Verlet, self-induced G) | 2026-10-07: isotropic multi-D softening, shape-safe acceleration, consistent imbalance statistic; 1-D numerics bit-identical |
| `src/__init__.py` | active | package marker | added Session 2 |
| `tests/test_physics.py` | active | 9 invariant tests | virial test = 2-D circular orbit (exact −0.5); history in docstring + F10 |
| `tests/conftest.py` | active | enables JAX float64 for the suite | required for I2/I4-class thresholds |
| `docs/00_INDEX.md` | active | master entry point | every agent starts here |
| `docs/ResearchLog.md` | active | chronological log, newest first | Session 2 entry = full audit |
| `docs/06_research/` | active | per-topic research (R-XXX-### registry in README) | R-PHY-001 ✅, 002/003/004 open/partial |
| `generate_docs.py` | active | doc generator: DOCS dict ↔ `docs/` tree | regenerate to verify: `python generate_docs.py --out /tmp/docs_check && diff -r docs /tmp/docs_check --exclude=.git` |
| `docs/<NN>_*/` | active | 12 numbered categories (47+3 docs) | reorganized 2026-10-07 via git mv |

## Environment (measured)
- Python 3.11.2 · jax 0.10.2 (CPU) · pytest 9.1.1 · numpy
- Bootstrap: `pip install "jax[cpu]" pytest` (sandbox needed `--break-system-packages`)
- No `pyproject.toml`, no CI, no dependency pins — future work.

## Known Issues & Open Items
- **CON-003 (OPEN, needs human ADR):** `compute_self_induced_G` returns magic
  `G = 1.0` in degenerate geometry; and `integrate()` freezes G from t=0 while
  Physics.md claims a running average — two different dynamical systems.
  Options (a/b/c) recorded in `08_failures/Conflicts.md`. Do not silently patch.
- **F10 (logged):** 1-D conservative configurations cannot satisfy any
  collision-resolved invariant test (radial plunge → numerical heating).
  All future conservative tests must pass the preflight described in
  `06_research/physics/orbital_conditions.md`.
- CON-001 ✅ resolved (Session 1); CON-002 ✅ resolved (Session 2, R-PHY-001).
- Legacy Persian docs kept verbatim: `11_meta/goal.md`,
  `12_prompts/master_prompt.md`, `06_research/open_problems.md`, plus the
  pre-protocol formulas inside `04_market/Detectors.md` / `MarketMaking.md` /
  `07_hypotheses/Experiments.md` — these contain spec content that VIOLATES
  current axioms (z-scores, seconds, magic constants); re-derivation is
  scoped in `06_research/detectors/*` and `06_research/market_making/*`.
  Earlier sync claim "all docs translated" was false.

## Open Questions (physics)
- Which reading of Axiom 4 governs: frozen-initial G (conservative, testable)
  or running-average G (adaptive, non-conservative)? → R-PHY-002 / T-010.
- Is `G = 1/⟨d²⟩` self-consistent off-circular orbits? (For a single pair it
  makes V ∝ −1/d³ effectively — homogeneity exponent n = −3 ⇒ time-averaged
  ratio −3/2, not −1/2. Circular orbits hide this because ⟨d²⟩ = d².) Needs
  an explicit experiment → R-PHY-002 E1.
- Can the generalized four-term identity (R-PHY-004) survive ε-guard and
  softening corrections at realistic tick dt? → T-008.

## Verified This Session (numbers worth reusing)
- 2-D circular orbit (m=1, d=2, G=0.25, v=0.25/body): T = 0.0625,
  V = −0.125, T/V = −0.5 exactly; leapfrog deviation ~1e−10; E drift ~5e−14;
  L = 0.5 constant to 1e−14.
- Eccentric exact-integer-period averages (dt = 2e−5): deviation from −0.5:
  k=0.95 → 5e−10 · k=0.9 → 3e−8 · k=0.8 → 7e−8 (1 period), 2e−9 (10 periods);
  k=0.6 → 1.4e−7 · k=0.5 → 7.4e−8. Escape boundary v/v_circ = √2.

## Next Session Entry Point
`docs/09_agents/AgentHandoff.md` (Session Packet, top) → pick T-008/T-009/T-010.
