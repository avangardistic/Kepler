# Roadmap

> This is a dependency plan, not evidence that a phase works. The repository's implementation and measured results take precedence over planned milestones. No phase authorizes trading or order execution.

## Current state

- **Phase 0 — Foundations:** documentation exists; the theoretical claims remain hypotheses.
- **Phase 1 — Tick infrastructure:** implemented. The offline 100,000-tick retention acceptance test passes in the recorded environment; a 2,785-tick live capture is committed. A full 100,000-tick live run has not been completed.
- **Phase 2 — Physics:** `src/physics_jax.py` and synthetic invariant tests exist. **Real-data validation is not complete:** I1/I2 fail on the captured replay at `dt = 1`; see CON-008/F10. Resolve the model question before claiming success.
- **Phase 3 — Detectors:** not implemented. T-005 is open and can be developed on stored L2 ticks without relying on the physics invariants.
- **Phase 4 — Market-making proposal:** not implemented and currently conflicts with the project's anti-goals if it produces actionable quotes/signals. Keep blocked pending an explicit scope decision; no exchange execution is allowed.
- **Phases 5–10:** proposed simulation, validation, and mathematical extensions; not implemented. Phase 5's `Π` result is blocked by CON-008 and by the need to define the experiment precisely.

The test count and environment below are historical verification evidence, not a promise that tests have run in the current checkout. See [`../03_research/ResearchLog.md`](../03_research/ResearchLog.md) for dated evidence.

## Phases and gates

| Phase | Focus | Gate before calling it complete |
|---|---|---|
| 0 | Definitions, assumptions, and falsifiability | Claims have explicit definitions and rejection criteria; untested claims remain labelled |
| 1 | Raw L2 capture, bounded storage, deterministic replay | Offline 100,000-tick test has zero drops/order errors; storage fidelity and replay determinism pass. Live coverage is reported separately |
| 2 | Physics implementation and invariants | Synthetic and real-data behavior are reported separately; CON-008 is resolved by an explicit decision and re-measurement before any real-data pass is claimed |
| 3 | Research detectors | Synthetic evaluation is reproducible; metrics, data split, and leakage controls are specified |
| 4 | Any non-executing market-making mathematics | Scope is explicitly approved, formulas have no unexplained free parameters, and no code emits actionable trading outputs |
| 5 | Long-run simulation of the mathematical model | CON-008 is resolved; `Π` is defined; simulation and statistical protocol are reproducible |
| 6 | Hypothesis validation | Experiments, baselines, uncertainty, and rejection criteria are set before inspecting outcomes |
| 7–8 | Geometry / gauge / multidimensional extensions | Each extension is motivated, derived, and independently falsifiable; analogy alone is not evidence |
| 9 | Documentation / publication | All reported results trace to code, data provenance, commands, and measured outputs |
| 10 | Synthesis | Only after earlier claims survive their tests; no claim of a unified theory by roadmap declaration |

## Next work

1. Record a maintainer decision for **CON-008** before further real-data claims about I1/I2 or Phase 5.
2. **T-005** is the next unblocked implementation task in [`TaskQueue.md`](TaskQueue.md).
3. **T-006** remains blocked by the scope mismatch between quote generation and the project's anti-goals.
4. Improve replay-to-state throughput only with a before/after benchmark and unchanged behavior.

No calendar estimates are provided: the next gates depend on evidence and an unresolved model decision, not elapsed time.
