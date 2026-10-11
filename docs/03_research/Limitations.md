# Limitations

This file describes boundaries of the current data and implementation. It is not a complete list of market risks.

## Data visibility

- The current pipeline uses a single venue's `depth20@100ms` snapshots, not full order-by-order events or the complete order book.
- Snapshots for different symbols arrive asynchronously; latest-wins replay is deterministic but not simultaneous sampling.
- The selected payload does not provide an exchange event timestamp. Local receive time is provenance, not model time.
- L2 data cannot represent news, hidden liquidity, off-venue activity, or all causes of price movement.
- Network interruptions, stale books, and feed-level artifacts may affect observations; they must be reported, not assumed away.

## Model and implementation

- The three-body mapping is a model hypothesis, not a physical law. Terms such as mass, force, and gravity are analogies with explicit mathematical definitions.
- The code's self-induced `G` is held from the initial state, while the theory describes a running average (CON-005 remark).
- ADR-008's rigid-rotation embedding is exact for two bodies, not general three-body input.
- The captured real-data replay fails I1/I2 on tested paths at `dt = 1` (CON-008/F10). A passing synthetic test does not remove this limitation.
- The replay-to-state path was measured as a performance bottleneck; see the research log/task queue for the recorded environment and measurement.
- The committed live sample has 2,785 ticks; the full 100,000-tick live acceptance run is not recorded as complete.

## Scope exclusions

No exchange execution, quote delivery, fill model, fee/impact model, position-capacity model, financial risk control, or realized P&L validation is implemented. Their absence is not evidence of safety, zero drawdown, or profitability.

## Interpretation rule

A conclusion is limited to its exact data source, code version, model path, metric, and test protocol. Do not generalize a synthetic result to live market behavior or a small capture to a market-wide claim.
