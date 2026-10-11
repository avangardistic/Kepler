# Philosophy and Scope

## Project identity

Kepler is an offline mathematical research project. It tests whether three-body geometry can describe selected behavior in raw L2 order-book data. The analogy is a hypothesis, not an established physical law.

The project does not execute trades, issue trading signals, predict prices, provide investment advice, or claim realized profit.

## Working principles

### Raw input and explicit transformations

Use raw L2 snapshots as modeled input. Any derived state or transformation must be visible, documented, and testable; do not silently add indicators or filters and call the result raw data.

### Discrete time

Use ticks as the model's time unit. Feed time stamps may be preserved as provenance, but do not substitute seconds/candles for tick time without a reviewed decision.

### Geometry as a lens, not proof

The model represents assets as bodies in a geometric state space. Statements such as “the orbit is a filter,” “gravity is an indicator,” or “the market is a field” are metaphors or hypotheses; they require measurable definitions before they can support a result.

### No hidden parameters

Physical/model parameters must follow the documented derivation or be recorded as an explicit unresolved choice. Infrastructure settings are not automatically physical parameters.

### No risk-safety claim

The repository intentionally contains no trading risk controls because trading is out of scope. Their absence does not imply that geometry solves risk or makes trading safe.

## Research questions

- Are the proposed states and forces useful descriptions of L2 behavior?
- Which invariants survive on real replay, not just purpose-built synthetic states?
- Does the conservative virial relation hold under its stated assumptions?
- Can the proposed work functional be defined and tested without turning it into a trading-profit claim?

## Anti-goals

- Trading or order execution
- Actionable quotes or signals for trading
- Price prediction or a sellable strategy
- Treating synthetic success as real-market validation
- Treating an open conflict as resolved for convenience

## Falsifiability

A failed invariant, unsupported assumption, or negative experiment is a useful result. The real-data I1/I2 failures are recorded in [`../03_research/Conflicts.md`](../03_research/Conflicts.md) CON-008 and must remain visible until a model decision and re-test are recorded.
