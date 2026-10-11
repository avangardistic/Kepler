# Project Goal and Boundaries

## Research objective

Test whether three-body dynamics applied to raw Level 2 (L2) order-book snapshots can provide a useful **descriptive** vocabulary for selected high-frequency market-microstructure behavior. The objective is falsifiable; the model is not established merely because the code runs or a synthetic test passes.

## Scope constraints

- **Input:** raw L2 snapshots. Do not add derived indicators, filters, external features, or hidden calibration parameters as model inputs.
- **Time:** discrete ticks as defined in [`../01_theory/TickModel.md`](../01_theory/TickModel.md).
- **Model parameters:** derive from the stated model geometry or document and review any exception. Infrastructure settings (such as buffer size or endpoint) are not physical parameters.
- **Use:** offline research and measurement only. No order placement, live trading, signal service, price prediction, investment advice, or claims of realized profit.
- **Risk:** the project does not implement financial risk controls and does **not** claim geometry makes trading safe. No deployment or capital use is in scope.

## Claims to test, not assume

| Claim | Evidence required | Current status |
|---|---|---|
| Angular momentum remains bounded in the intended conservative model | Reproducible tests and real-data replay under a documented model | Synthetic tests exist; real-data behavior is part of open CON-008 |
| The conservative virial ratio approaches `-1/2` | A defined conservative experiment and unchanged acceptance criterion | A purpose-built test exists; this is not a real-data result |
| The mathematical work functional `Π` has positive expectation | A precise definition, pre-registered experiment, and uncertainty interval | Not tested |
| Empty/jumpy books trigger the stated self-freeze behavior | A defined implementation and tests | Empty-depth handling exists in parts of the physics path; the broader criterion is not established |

The 2026-10-11 real-data replay recorded in [`../03_research/Conflicts.md`](../03_research/Conflicts.md) CON-008 falsifies the current claim that I1/I2 hold for every real-data path at `dt = 1`. Keep that result visible; do not describe the model as validated until the conflict is resolved and the data are re-evaluated.

## Anti-goals

- Trading bot or exchange execution
- Quote/signal service intended for trading
- Price-prediction product
- Sellable or production strategy
- Treating model output as a substitute for risk management

A non-executing mathematical proposal may be studied only when it is explicitly labelled as a proposal, its assumptions are listed, and its claims are tested. See [`../02_engineering/MarketMaking.md`](../02_engineering/MarketMaking.md) for the status of the legacy market-making sketch.
