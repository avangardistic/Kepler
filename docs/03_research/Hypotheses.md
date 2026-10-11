# Hypotheses

> The entries are proposed claims, not accepted facts. No result is implied by the existence of a rejection criterion. Any hypothesis involving quote volume or trading profitability is blocked by the current project scope; see CON-009.

| ID | Claim (testable only after precise definitions) | Rejection criterion | Status |
|---|---|---|---|
| H1 | Angular momentum remains bounded in a specified conservative model | Use the I1 criterion in `../01_theory/Invariants.md` over a prespecified horizon | Synthetic tests exist; real-data behavior is open under CON-008 |
| H2 | The conservative virial ratio approaches `-1/2` | Use the I4 criterion in `../01_theory/Invariants.md` after a prespecified equilibration period | Purpose-built synthetic test exists; not established on real data |
| H3 | A defined mathematical work functional `Π` is associated with a stated geometric quantity | Define both quantities and test a preregistered association criterion with uncertainty; do not call `Π` realized profit | Not defined or tested |
| H4 | Empty/degenerate model states map to a zero/frozen state | Define “freeze” independent of quote output and test edge cases | Partially implemented for zero-depth physics input; broader claim unverified |
| H5 | The model returns to a specified state after a defined gap | Define gap, distance metric, data, and recovery criterion before testing | Not tested; current wording is underspecified |
| H6 | The proposed state representation behaves as intended across defined L2 regimes | Prespecify the regime taxonomy and per-regime criteria | Not tested |
| H7 | The proposed hedge constraint is preserved | Define the constraint and a model-only test without execution | Not implemented/validated |

## Protocol

For each experiment, record the exact dataset or generator, code revision, metric, rejection criterion, and command before inspecting outcomes. Separate synthetic, replay, and live-feed evidence. If a claim is not measurable yet, refine its definition before collecting data; do not select a threshold after seeing the result.
