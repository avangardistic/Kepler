# Falsifiability

## Principle

Every scientific claim must be capable of failing under a stated observation. A test is useful only if the metric, population, and rejection criterion are defined before interpreting results.

## Claims and current status

| Claim | Rejection signal | Status |
|---|---|---|
| I1 — bounded angular momentum | Violates the criterion in `../01_theory/Invariants.md` under the declared model/data protocol | Synthetic tests exist; real-data behavior is part of open CON-008 |
| I2 — energy conservation for a closed conservative subsystem | Relative drift exceeds the fixed I2 criterion under stated conservative assumptions | Synthetic test exists; real-data replay fails in the documented paths |
| I4 — standard virial ratio | `|⟨T⟩/⟨V⟩ + 1/2|` exceeds the fixed criterion in the declared conservative subsystem | Synthetic test exists; no real-data pass is established |
| Positive expectation of mathematical `Π` | A prespecified uncertainty interval supports a non-positive expectation | Not testable until `Π` and the sampling protocol are defined; do not call it realized profit |
| Empty-state freeze | A defined empty input fails to produce the specified frozen model state | Some zero-depth handling exists; the full property needs a precise test |

## Known counterevidence

The live L2 fixture replay at `dt = 1` fails I1/I2 criteria on the measured paths. This is documented as CON-008 and F10. The result is not invalidated by passing synthetic tests; no threshold is changed to reconcile the two.

## Scope boundary

Claims about quotes, trading volume, realized profitability, drawdown, or “risk solved” are not current acceptance criteria. They require a maintainer-approved scope change and must never be inferred from an offline mathematical functional.

## Reporting

For each result, state the data source, model path, code version, metric, threshold, and limitations. Use “not tested” or “inconclusive” when appropriate; do not force every outcome into pass/fail.
