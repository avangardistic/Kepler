# Axioms and Model Claims

> This file separates project constraints from scientific claims. A statement here is not evidence that the model works; the status of a tested claim is in [`Invariants.md`](Invariants.md), [`../03_research/Conflicts.md`](../03_research/Conflicts.md), and the dated research log.

## Project constraints

### Axiom 1 — Raw L2 Input
The modeled market input is raw L2 order-book snapshots. Do not add hidden indicators, filters, external features, or derived fields to stored raw ticks. Derived model state may be computed explicitly during analysis/replay.

### Axiom 2 — Tick Time
Model time is discrete and measured in ticks. The mapping from feed events to ticks is defined in [`TickModel.md`](TickModel.md) and ADR-011.

### Axiom 9 — Falsifiability
Every scientific claim must have a stated observable, experiment, and rejection criterion. A model claim without a test is a proposal, not a result.

### Axiom 10 — No Execution
This repository is for offline research. It must not place orders, trade, or present itself as a live execution system.

## Model definitions and hypotheses

### Axiom 3 — Mass from Book Depth
The current model defines mass as `m_i = ln(1 + D_i)`, where `D_i` is the specified L2 depth quantity. This is a modeling choice, not a measured physical mass.

### Axiom 4 — Self-Induced Coupling
The intended coupling is derived from the model's geometry, without an unexplained free physical parameter. The exact time dependence is unresolved: the implementation holds the value computed from the initial state, while the theory text describes a time average (CON-005 remark).

### Axiom 5 — Hedge Constraint (proposal)
The model proposes deriving a hedge relation from mass ratios. No hedge execution exists; the constraint is not a validated operational rule.

### Axiom 6 — No Trading Risk Controls
No financial risk-management or trading-control system is implemented. This is a project-scope exclusion; it does **not** mean risk is solved by geometry or that the model is safe to trade.

### Axiom 7 — Mathematical Work Functional
`Π = ∮ p · dx` is a proposed mathematical functional. It is not realized profit, P&L, or evidence of profitability. Its operational experiment remains undefined.

### Axiom 8 — Virial Relation (conditional hypothesis)
The standard `⟨T⟩/⟨V⟩ → -1/2` relation applies to the stated conservative subsystem, not automatically to systems with friction or imbalance. It remains a model claim; synthetic test results do not establish real-data validity. See I4 in [`Invariants.md`](Invariants.md) and open CON-008.

## Review rule

If an implementation, measurement, or accepted decision contradicts one of the model claims, record the conflict and evidence. Do not edit a criterion merely to make the contradiction disappear.
