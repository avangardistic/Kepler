# Prior Art

> Notes on related work and on how this project differs. The "difference" and
> "what's new" lists describe **proposed** positioning; the market-making parts
> are not implemented and T-006 is blocked (CON-009).

## Physical Models of Markets
- **Econophysics** (Stanley, Mantegna): Power-law distributions in returns.
- **Ising model** (Bornholdt): Phase transitions in markets.
- **Coupled oscillators** (Sornette): Synchronous oscillations.

## Three-Body Models in Finance
- **Triangular arbitrage** as three-body (Zhou et al.)
- **Cross-currency dynamics** with Lotka-Volterra equations.
- **Network triplets** (Aste).

## Modern Market Making
- **A-S (2008)** with inventory risk.
- **Guéant-Lehalle-Fernandez-Tapia (2013)** with constraints.
- **Cartea-Jaimungal** with value function.

## Difference of This Project (as proposed)
1. Combination of **three-body + market making + L2** — the market-making part is not implemented (T-006 blocked, CON-009).
2. **No trading risk controls**: a scope exclusion only (ADR-005). Risk is **not** solved by geometry, and no safety claim is made (CON-010).
3. **No filter**: self-adaptation is a design intent, not a validated property.
4. **Tick-based**: time quantization.
5. **Mathematical game**: never executed.

## What's New? (proposals, not results)
- A-S mapping to three-body via $\gamma = 1/\|\vec L\|$ — an unvalidated draft mapping in [`../02_engineering/MarketMaking.md`](../02_engineering/MarketMaking.md).
- Hedge = mass ratio (not decision) — proposal only (Axiom 5).
- Grid = actual L2 levels (not computational distance).
- Self-freeze at $\|\vec L\| = 0$ — the empty-depth handling exists in the physics path; the broader self-freeze criterion is not established (see Falsifiability.md).
