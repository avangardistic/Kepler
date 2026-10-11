# Market-Making Proposal — Scope Blocked

> **Status:** Unimplemented, unvalidated, and not approved for operational use. This document records a research proposal only. The project's current anti-goals prohibit a trading or actionable quote/signal service; T-006 is blocked pending a maintainer scope decision.

## Historical model mapping

The previous draft mapped an Avellaneda–Stoikov-style formulation onto the three-body model:

| Classical quantity | Proposed mapping | Status |
|---|---|---|
| Risk aversion `γ` | `1 / ‖L‖` | Unvalidated; not a risk control |
| Inventory `q` | `m · v` | Proposed analogy only |
| Price `s` | position `x_i` | Requires a defined transform back to price |
| Volatility `σ²` | `‖F_i‖ / m_i` | Dimension/meaning not validated |
| Fill intensity `k` | constant | Unspecified external parameter; conflicts with no-hidden-parameter rule |

The draft also used `T`, `κ`, and `k` in spread/size formulas without an accepted derivation. Those formulas are not an approved specification and are intentionally not repeated as executable instructions here; the historical equations remain in `../01_theory/Strategy.md` for traceability.

## Why implementation is blocked

- Producing bid/ask prices or sizes can become an actionable signal, which conflicts with [`../04_planning/goal.md`](../04_planning/goal.md).
- No execution, fill, fee, impact, or inventory model exists.
- The real-data I1/I2 conflict (CON-008) remains open.
- No Sharpe, P&L, drawdown, or “risk solved” claim is supported by the repository.

## Required decision and acceptance

Before any code is written, the maintainer must decide whether strictly offline, non-actionable study of the equations is within scope. If so, update the project goal and an ADR, define every variable and parameter, specify data/simulation protocol and rejection criteria, and ensure no output can be used as live quotes. Otherwise retire T-006 and keep this file as a historical note.
