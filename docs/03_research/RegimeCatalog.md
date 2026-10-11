# Regime Catalog

> **Status:** Draft taxonomy only. No regime classifier, detector, or automatic
> response is implemented, and nothing here is a trading instruction. The
> "Automatic Response" column describes the *intended conceptual* mapping; the
> detector draft in [`../02_engineering/Detectors.md`](../02_engineering/Detectors.md)
> has not been reconciled with the tick-time/no-filter constraints and T-005 is
> still open. The parameter table is illustrative: its values are not derived
> from the model geometry and would violate the no-hidden-parameter rule
> (Axiom 4) if used as implementation constants.

## Ten L2 States

| # | State | Signature | Automatic Response |
|---|-------|-----------|--------------------|
| 1 | Balanced | $I \approx 0$ | Symmetric grid |
| 2 | Bid-heavy | $I > 0.3$ | Short hedge |
| 3 | Ask-heavy | $I < -0.3$ | Long hedge |
| 4 | Thin | Small $m$ | Weak gravity |
| 5 | Thick | Large $m$ | Strong gravity |
| 6 | Spoof | z-score > 3 | Fake mass removed |
| 7 | Iceberg | refresh ≥ 3 | Hidden mass added |
| 8 | Sweep | One side empty | Gauge rotation |
| 9 | Flash | Depth → 0 | Freeze |
| 10 | Squeeze | Sharp $I$ | Anti-gravity |

## Parameter Table (illustrative, not implementation constants)

| State | $m$ | $I$ | $\gamma$ | $\|\vec L\|$ | Spread |
|-------|-----|-----|----------|--------------|--------|
| Balanced | 5 | 0 | 1e-3 | Medium | Tight |
| Bid-heavy | 5 | +0.5 | 1e-3 | High | Tight |
| Ask-heavy | 5 | -0.5 | 1e-3 | High | Tight |
| Thin | 0.5 | — | 1e-3 | Small | Wide |
| Thick | 20 | — | 1e-3 | Large | Tight |
| Spoof | 5 | — | 1e-3 | Irregular | Medium |
| Iceberg | 8 | — | 1e-3 | Medium | Tight |
| Sweep | 3 | ±0.8 | 5e-3 | Spike | Wide |
| Flash | 0.1 | — | 1e-2 | Zero | Freeze |
| Squeeze | 1 | +0.9 | 5e-3 | Unstable | Wide |
