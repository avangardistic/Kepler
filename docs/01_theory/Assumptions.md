# Assumptions and Validity Boundaries

> These are candidate modeling assumptions to test, not guarantees about markets or exchange feeds. Execution-related assumptions from the original draft are retained only as out of scope; no trading execution is implemented.

## Data and replay assumptions

1. **Snapshot scope:** the current client consumes Binance `depth20@100ms` snapshots, not a complete reconstructed order book. It preserves the payload's available levels.
2. **Asynchronous symbols:** BTC, ETH, and SOL snapshots arrive at different times/rates. Replay uses the latest observed snapshot per symbol; this is a documented alignment choice, not simultaneous sampling.
3. **Feed timestamps:** the selected snapshot payload has no exchange event timestamp; `ts_exchange_ns = 0` means unavailable for this feed. Local receipt time is provenance only.
4. **Retention:** ticks may be stored and replayed only if ordering and field-fidelity checks pass. A captured dataset does not establish that model invariants hold.
5. **Single-feed scope:** cross-exchange consistency, complete market depth, and exogenous information are not modeled by the current pipeline.

## Model assumptions needing evidence

- A depth-derived mass and microprice-derived position are useful state variables.
- A chosen geometric force/coupling can describe the observed dynamics without unexplained free parameters.
- Results from a conservative synthetic subsystem may help characterize the integrator, but cannot be generalized to real data without replay validation.
- Current real-data tests expose failures in I1/I2 at `dt = 1`; see CON-008. These are not to be hidden by this assumptions list.

## Explicitly out of scope

The old draft assumed constant fees, no market impact, infinite position capacity, no counterparty risk, and guaranteed complete/low-latency data. Those are execution assumptions, not facts established by this research. Because Kepler does not execute or model live positions, none should be used to imply operational safety or profitability.

## Validity boundary

A result applies only to the data, transformations, model version, and experiment protocol actually tested. Report feed gaps, asynchronous alignment, capture size, and known failure modes alongside every conclusion.
