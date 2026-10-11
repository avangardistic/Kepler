# Experiments

> **Status:** Proposal catalogue. The experiments below are not evidence of completed work. Do not run a trading-performance comparison under this project scope. Define and review each protocol before looking at the outcome.

| ID | Question | Proposed data | Status / gate |
|---|---|---|---|
| E1 — Long-run simulation | Does a precisely defined mathematical work functional `Π` have positive expectation under the model? | Reproducible stored/replayed L2 data plus a defined simulation | Not ready: CON-008 open; define `Π`, baseline, sampling, and uncertainty first. No realized-profit interpretation. |
| E2 — Regime response | Does the model state respond consistently to a declared set of L2 regimes? | Controlled synthetic states | Not designed: specify regime labels and per-state acceptance criteria before running. |
| E3 — Gap/failure response | What happens to the model state after a defined discontinuity or empty book? | Controlled fixture and/or captured replay | Not designed: define gap and “recovery”; do not claim a self-freeze property without a test. |
| E4 — Conservation | Which invariants hold in a conservative subsystem and in real-data replay? | Synthetic conservative subsystem and committed capture, analysed separately | Synthetic tests exist; real-data I1/I2 failure is documented in CON-008/F10. |
| E5 — Classical-model comparison | Is a model-only descriptive statistic different from a specified baseline? | Same fixed data and predeclared metrics | Prior “higher Sharpe” proposal is out of scope: it implies trading-performance evaluation. Do not use Sharpe/P&L without a revised project scope. |
| E6 — Sampling/time-scale sensitivity | How do results vary under a clearly defined tick mapping? | Same ordered raw input | Not designed; tick-time rule is fixed unless an ADR revises it. |
| E7 — Multidimensional extension | Does a declared multi-dimensional state remain numerically stable? | Reproducible synthetic and replay inputs | Proposed only; requires earlier model decisions. |

## Statistical protocol checklist

Before running an experiment, record:

- the question and one falsifiable hypothesis;
- dataset provenance, code version, and inclusion/exclusion rules;
- baseline and metric, including units/definition;
- rejection criterion and uncertainty method;
- confounders, dependence structure, and any multiple-testing correction;
- exact command and expected artifact.

A paired test, bootstrap, or correction method is not automatically valid just because it appears in a plan; justify it for the data and question. Preserve negative and inconclusive outcomes.
