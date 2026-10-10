# Prior Art

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

## Difference of This Project
1. Combination of **three-body + market making + L2**.
2. **No risk management**: Risk in geometric constraint.
3. **No filter**: Self-adaptation.
4. **Tick-based**: Time quantization.
5. **Mathematical game**: Never executed.

## What's New?
- A-S mapping to three-body via $\gamma = 1/\|\vec L\|$.
- Hedge = mass ratio (not decision).
- Grid = actual L2 levels (not computational distance).
- Self-freeze at $\|\vec L\| = 0$.
