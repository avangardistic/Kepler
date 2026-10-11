# Strategy Sketch — Not Approved for Use

> **Status:** Historical mathematical proposal only. It is not implemented, tested, or approved as a signal/quote generator. Under the current project goal, T-006 is blocked. No formula below may be connected to an exchange or used to make trading decisions.

## Scope

This file preserves the outline of an offline market-making analogy for research traceability. Its presence is not a recommendation, trading strategy, or evidence that any output is profitable or safe.

## Legacy equations (unvalidated)

The earlier draft proposed a reservation value:

$$
r_i = x_i - (m_i v_i) \cdot \frac{1}{\|\vec L\|} \cdot \frac{\|F_i^\text{grav}\|}{m_i} \cdot (T-t)
$$

and a spread:

$$
\delta_i = \frac{\sigma_i^2}{\|\vec L\|}(T-t) + 2\|\vec L\|\ln\!\Big(1 + \frac{1}{k\|\vec L\|}\Big).
$$

It also proposed deriving bid/ask offsets, size, and a hedge from imbalance, mass, and angular momentum. None of those outputs exist in `src/`.

## Unresolved issues

- `T`, `k`, `κ`, `σ`, and the mapping from model state to quoted prices are not fully defined or validated; some may act as free external parameters.
- A quote-generation output conflicts with the current anti-goal of avoiding actionable trading signals.
- The model's real-data I1/I2 failure (CON-008) undermines using these equations as a validated downstream model.
- No fill, fee, market-impact, inventory, or execution model exists; therefore no P&L, Sharpe, drawdown, or profitability result can be inferred.

## Gate before further work

A maintainer must explicitly reconcile this proposal with [`../04_planning/goal.md`](../04_planning/goal.md), document the scope decision, and define a strictly offline experiment before T-006 can proceed. Until then, do not implement `quote_all` or produce actionable quotes.
