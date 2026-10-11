# Conflicts

## Current status

Open: **CON-008** (model decision), **CON-009** (scope decision), and **CON-011** (implementation vs documented L2→state formulas). CON-010 is closed as a documentation clarification. A conflict may remain open at handoff; do not resolve it without evidence or a maintainer decision.

## CON-001: ADR-007 G_DEFAULT violates Axiom 4
**Date:** 2026-10-07
**Files:** `docs/Decisions.md` (ADR-007) vs `docs/Axioms.md` (Axiom 4)
**Description:** ADR-007 introduced G_DEFAULT = 1e-6 as a magic constant for log-price positions. This violates Axiom 4 which requires self-induced gravity without free parameters.
**Severity:** HIGH
**Resolution proposed:** Reject ADR-007. Implement G_eff = 1 / <d²>_t (time-averaged squared distance). Update Physics.md with self-induced gravity formula.
**Status:** RESOLVED — ADR-007 rejected, Physics.md updated.

## CON-002: Virial test threshold loosening (resolved)
**Date:** 2026-10-07
**Files:** `src/physics_jax.py` tests vs `docs/Invariants.md` (I4)
**Description:** Workflow confusion: an earlier migration pass log stated that the test
threshold was "loosened to 1e-5" to make tests pass. That never happened in the
codebase. `test_virial_ratio_convergence` has always evaluated I4 as
`|<T>/<V> + 0.5| < 0.2` (the invariant criterion from Invariants.md) over a
20,000-tick conservative two-body subsystem with dt = 0.001. The log entry was a
writing error, not a threshold change.
**Severity:** MEDIUM (log accuracy only; no code or invariant threshold changed)
**Resolution:** Log corrected. Invariants.md now documents both the standard virial
form (I4) for conservative subsystems and the generalized form (I4b) for systems
with external forces and friction. Physics.md documents the generalized form and
notes when each applies. The test remains unchanged and passes.

## CON-003: Energy test precision (float32 vs I2 criterion)
**Date:** 2026-10-10
**Files:** `src/physics_jax.py` (JAX default precision) vs `docs/Invariants.md` (I2, relative drift < 1e-9) and `docs/Decisions.md` (ADR-002: "JIT + x64 + vmap")
**Description:** Under JAX's default float32, `test_energy_conservation_relative_drift` fails with max relative energy drift 8.01e-08 (float32 eps ≈ 1.2e-7 cannot meet 1e-9). With `JAX_ENABLE_X64=1` all 9 tests pass. The ResearchLog entry of 2026-10-07 stated "absolute drift < 1e-5", which does not match the I2 criterion.
**Severity:** HIGH (test failing on default configuration)
**Resolution:** x64 enabled in `physics_jax.py` via `jax.config.update("jax_enable_x64", True)`, as prescribed by ADR-002. Verified: 9/9 tests pass without environment variables.
**Status:** RESOLVED — 2026-10-10. Correction logged in ResearchLog.md and Changelog.md.

## CON-004: Undocumented transverse velocity injection (RESOLVED)
**Date:** 2026-10-10
**Files:** `src/physics_jax.py` `_stabilized_state` (previously `v_y = 0.25·sign(v_x)`) vs `docs/goal.md` ("All parameters derived internally from geometry", "No external parameters").
**Description:** The constant `0.25` was not derived from geometry and was not documented. It also produced a non-zero angular momentum (≈ 0.5) while the test comment claimed L ≈ 0. Removing it outright broke `test_virial_ratio_convergence` (⟨T⟩/⟨V⟩ ≈ −252400).
**Human decision:** Derive the transverse velocity from geometry (option 2). Chosen 2026-10-10 by the project owner; formula chosen under the instruction to "use the most precise formulas".
**Resolution:** Rigid rotation about the mass centre with ω fitted to the self-induced gravity (ADR-008, Physics.md §Embedding). Constant removed. Test comment corrected; threshold unchanged. All 9 tests pass.
**Status:** RESOLVED — 2026-10-10.

## CON-005: Self-induced G normalisation mismatch (RESOLVED, one open remark)
**Date:** 2026-10-10
**Files:** `src/physics_jax.py` `compute_self_induced_G` (divided by the number of pairs) vs `docs/Physics.md` §Self-Induced Gravity (divides by N, the number of bodies).
**Description:** The two normalisations are identical for N = 3 (the target three-asset system) and differ for N = 2 (test-only subsystem). Measured: if the rotation used the Physics.md G while `integrate` used the code G, the two-body virial test failed (⟨T⟩/⟨V⟩ ≈ −2.39 over 200k ticks), because the velocities and the forces were computed with different couplings.
**Resolution:** Code aligned to Physics.md (1/N) in one shared helper `_self_induced_G_from_positions`, used by both the rotation and `compute_self_induced_G`. Consistency verified: two-body virial test passes.
**Status:** RESOLVED — 2026-10-10.
**Open remark (not changed):** Physics.md specifies a running time-average of ⟨d²⟩_t. The code uses the value from the initial state, held fixed in `integrate` (documented in its docstring). This is a known gap and needs a decision if the running average is required.

## CON-006: Six documentation files were cyclically mis-filed (RESOLVED)
**Date:** 2026-10-11
**Files:** `README.md`, `docs/prompt.md`, `docs/TaskQueue.md`, `docs/ResearchLog.md`, `docs/Changelog.md`, `docs/AgentSync.md`
**Description:** Commit `829a846` ("Sync main branch with arena/ff347927-kepler documentation updates and status audit") wrote the content of six documents into the wrong paths, each shifted by one position:

| File | Content actually present before the fix |
|------|----------------------------------------|
| `README.md` | the agent entry prompt |
| `docs/prompt.md` | the task queue |
| `docs/TaskQueue.md` | the research log |
| `docs/ResearchLog.md` | the changelog |
| `docs/Changelog.md` | the agent synchronisation table |
| `docs/AgentSync.md` | an older revision of the README |

The contents were the *newest* revisions (the 2026-10-10 sync notes were present), so nothing was lost by the merge, but the paths were wrong. `MISSION_PROMPT.md` §5 instructs an incoming agent to read the task queue from `docs/TaskQueue.md` and claim its task in `docs/AgentSync.md`; both files delivered unrelated content. The previous audit (2026-10-10) had already found documentation drift of the same family (stale `prompt.md`, wrong task states), so the pattern is recurring.
**Severity:** HIGH (an onboarding agent cannot find the task queue, the sync table, the changelog or the README)
**Resolution:** Contents restored to their canonical paths (a pure rotation; no text was edited except by later entries). `README.md` was restored to the newer `# Kepler` revision from `829a846^`, which documents `docs/prompt.md` as the entry prompt.
**Status:** RESOLVED — 2026-10-11. Root cause is a rename/copy script that shifted filenames; no code impact, tests were unaffected (9 passed before and after).

## CON-007: `ts_exchange` is documented as required but the chosen feed carries no exchange timestamp (RESOLVED)
**Date:** 2026-10-11
**Files:** `docs/DataSpec.md` §Normalized Fields (`ts_exchange | int ns | Exchange time`) vs the `depth20@100ms` snapshot payload, which contains only `lastUpdateId`, `bids`, `asks` (no `E` field).
**Description:** T-001 had to map the normalized schema onto a real feed. Two options: (a) use the diff-depth stream `@depth@100ms`, which carries `E` but requires local book reconstruction — that is processing/filtering and therefore violates `docs/goal.md`; (b) use the snapshot stream `@depth20@100ms` and record that the exchange timestamp is absent.
**Severity:** MEDIUM (schema documentation vs feed reality; no model quantity depends on wall-clock time — time is ticks, Axiom 2)
**Resolution:** Option (b). `L2Tick.ts_exchange_ns` is 0 when the stream provides no event time, and `ts_local_ns` is always populated from the local clock. `docs/DataSpec.md` now documents both fields and the "0 = not provided by this stream" convention. No threshold or invariant was changed.
**Status:** RESOLVED — 2026-10-11 (documentation).

## CON-008: Invariants I1/I2 fail on real L2 data at dt = 1 tick (OPEN — needs a model decision)
**Date:** 2026-10-11
**Files:** `src/physics_jax.py` (`state_from_l2`, `_stabilized_state`, `acceleration`, `integrate`) vs `docs/Invariants.md` (I1, I2), `docs/Decisions.md` ADR-006 (time = tick) and ADR-008 (rigid-rotation embedding), measured on live data captured to Parquet by the new Phase 1 code.
**Description:** 2 785 live ticks (BTCUSDT/ETHUSDT/SOLUSDT, Binance `depth20@100ms`) were captured to Parquet and replayed. Integrating the resulting three-body state at `dt = 1` tick:

| Path (2 000 ticks, dt = 1) | ‖L‖₀ | ‖L‖ₘₐₓ | E₀ | max relative energy drift |
|---|---|---|---|---|
| 2-D `state_from_l2` output, conservative | 0 | 0 | −1.008 | 281 |
| 2-D `state_from_l2` output, with imbalance + friction | 0 | 6.25e4 | −1.008 | 6.2e6 |
| 1-D input ⇒ ADR-008 embedding, conservative | 8.484 | 8.484 | −0.6255 | 1.54 |
| 1-D input ⇒ ADR-008 embedding, with imbalance + friction | 8.484 | 1.65e6 | −0.6255 | 1e7 |

I2 requires a relative drift < 1e-9; every path misses it by many orders of magnitude. Two structural causes were identified:

1. **The ADR-008 embedding never runs for L2-built states.** `state_from_l2` returns `x` with shape `(3, 2)` (transverse component 0), while `_stabilized_state` injects the rigid rotation only when `x.ndim == 1`. So the stabilization that rescues the 1-D tests is bypassed by the actual pipeline. Applying it manually keeps L constant in the conservative case but still leaves the energy drift at 1.54, i.e. ADR-008's N ≥ 3 residual (previously unmeasured) is large on real data.
2. **The imbalance acceleration is isotropic.** `a_i = grav + I_i − γ_i v_i / m_i` adds the scalar `I_i` to every spatial component, so a non-zero imbalance injects angular momentum and energy that no invariant bounds (measured ‖L‖ → 1.65e6).

**Severity:** HIGH — Phase 5 (`Π > 0` over 10 M ticks) and the whole "descriptive language" claim rest on I1/I2 holding on real data.
**Evidence:** docs/FailureModes.md F10; live dataset captured 2026-10-11 (2 785 ticks, 0 invalid books, 20 levels per side).
**Candidate directions (need a decision, then an ADR; no threshold will be touched):**
1. Calibrate the integration time scale from geometry instead of `dt = 1` tick — but ADR-006 makes one tick the only time quantum, so this must be expressed as a geometric scale factor, not a tunable step.
2. Make the pipeline actually use the ADR-008 embedding for L2 states (1-D positions or an explicit embedding call) and measure the N ≥ 3 residual; if the residual is irreducible, redefine the 3-body embedding.
3. Resolve the CON-005 remark (running time-average of ⟨d²⟩ instead of initial-state G) and re-measure: G is currently frozen at the first tick, which is the largest structural deviation from `docs/Physics.md`.
4. Make the imbalance direction explicit (per-axis projection derived from book geometry) rather than adding the scalar to every component.
**Status:** OPEN — escalated to human. Not fixed in the T-001/T-002 session: each candidate changes the model and requires an ADR, per the conflict-resolution order.

## CON-009: Quote-generation proposal conflicts with research-only anti-goals (OPEN)
**Date:** 2026-10-11
**Files:** `../04_planning/goal.md` anti-goals vs `../01_theory/Strategy.md`, `../02_engineering/MarketMaking.md`, and T-006.
**Description:** The legacy documents specify bids, asks, and sizes, while the project excludes trading systems and actionable signals. No quote-generation module exists, but the task title and formulas could lead an agent to build one without resolving scope.
**Severity:** HIGH (scope and safety ambiguity; no code impact yet)
**Resolution needed:** A maintainer must either (a) explicitly approve a strictly offline, non-actionable mathematical study and update the goal/ADR, or (b) retire T-006 and leave the formulas as historical notes. Until then, do not implement `quote_all`, emit actionable quotes, or connect anything to an exchange.
**Status:** OPEN — T-006 is blocked.

## CON-010: “Risk solved by geometry” is unsupported and conflicts with offline scope (RESOLVED — documentation)
**Date:** 2026-10-11
**Files:** `../01_theory/Philosophy.md`, `../01_theory/Axioms.md` Axiom 6, `../02_engineering/Decisions.md` ADR-005 vs `../04_planning/goal.md`.
**Description:** Older wording said risk was solved by geometry even though the project has no risk-management or execution system and makes no safety claim. That statement was unsupported and could be read as a recommendation to trade without controls.
**Resolution:** Clarify that “no risk management” is an offline-scope boundary only. The docs now explicitly state that risk is not solved, no financial controls exist, and no result implies safety. No code, invariant, or threshold changed.
**Status:** RESOLVED — 2026-10-11 (documentation clarification only).

## CON-011: `state_from_l2` does not follow the documented L2→state formulas (OPEN — implementation/doc mismatch)
**Date:** 2026-10-11
**Files:** `src/physics_jax.py` (`state_from_l2._microprice`, `state_from_l2._gamma`) vs `../01_theory/Microprice.md`, `../01_theory/Concept.md` §2.2 and §2.5, and `../02_engineering/Decisions.md` ADR-001.
**Description:** The documented position is built from the standard level-1 microprice `P^μ = (q₁ᵃp₁ᵇ + q₁ᵇp₁ᵃ)/(q₁ᵃ+q₁ᵇ)`, which uses the best bid and ask **prices**. The implementation instead sums each side's whole price column and evaluates `(Q_a·Σp_b + Q_b·Σp_a)/(Q_a + Q_b)`, where `Σp` is the sum of the received level prices (up to 20 levels per side). That value is neither the documented level-1 microprice nor the documented volume-weighted mid; it shifts `x_i = ln P^μ` by a level-count-dependent term. Separately, `_gamma` divides the spread by that same log-price `x_i`, while `Concept.md` §2.5 defines `γ_i = (p₁ᵃ − p₁ᵇ)/P^μ` with the microprice as a price — so the friction coefficient is evaluated on a different scale than documented.
**Severity:** HIGH — this is the model input for every real-data state, and the recorded CON-008/F10 measurements were computed with this construction. Correcting it could change the I1/I2 outcomes.
**Evidence:** `_microprice` calls `_safe_sum_col(bids, 0)` / `_safe_sum_col(asks, 0)` (the price columns) and returns their log; `_gamma(spread, x_i)` receives that log value. No test asserts the microprice or gamma formula: the L2-built fixtures only check invariants, and the two-body virial test constructs its `ThreeBodyState` directly with `gamma = 0`.
**Decision needed:** (a) correct the implementation to the documented level-1 microprice and price-scaled friction, then re-run the CON-008 measurements; or (b) record the aggregate construction as the intended model input in an ADR and update Microprice.md/Concept.md/ADR-001 to match. Do not change this silently, and do not touch any invariant threshold.
**Status:** OPEN — maintainer decision required.

## Conflict Resolution Rules

1. Follow applicable platform/safety instructions and the maintainer's explicit, current scope decision.
2. Use source, tests, and data provenance to establish implementation facts; do not let prose override measured evidence.
3. Accepted ADRs govern engineering choices only within the project scope; they do not prove scientific claims.
4. If a scientific or scope question remains unresolved, keep it open in this file and ask the maintainer. Do not choose a convenient document or silently modify a threshold.

## History
| Date | Conflict | Resolution |
|------|----------|------------|
| 2026-10-07 | CON-001: G_DEFAULT violation | ADR-007 rejected |
| 2026-10-07 | CON-002: Virial test threshold loosening (log error) | Corrected log entry; test + invariants unchanged |
| 2026-10-10 | CON-003: Energy test fails under float32 | RESOLVED — x64 enabled (ADR-002) |
| 2026-10-10 | CON-004: Undocumented 0.25 transverse velocity constant | RESOLVED — rigid rotation from geometry (ADR-008) |
| 2026-10-10 | CON-005: G normalisation (pairs vs N) | RESOLVED — aligned to Physics.md (1/N) |
| 2026-10-11 | CON-006: six docs cyclically mis-filed by commit 829a846 | RESOLVED — contents restored to canonical paths |
| 2026-10-11 | CON-007: `ts_exchange` required by DataSpec but absent from depth20 snapshots | RESOLVED — documented 0 = not provided; ts_local always set |
| 2026-10-11 | CON-008: I1/I2 fail on real L2 replay at dt = 1 tick | **OPEN** — measured (F10); four candidate directions; maintainer decision required |
| 2026-10-11 | CON-009: quote-generation spec conflicts with anti-goals | **OPEN** — T-006 blocked pending scope decision |
| 2026-10-11 | CON-010: unsupported “risk solved by geometry” claim | RESOLVED — wording corrected; no code or threshold changed |
| 2026-10-11 | CON-011: `state_from_l2` microprice/gamma differ from the documented formulas | **OPEN** — maintainer decision required; no threshold touched |
