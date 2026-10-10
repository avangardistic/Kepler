# Experiments

## E1 — 10 Million Tick Simulation
**Goal:** Test H1, H2, H3.
**Data:** Binance BTC/ETH/SOL.
**Criterion:** $\Pi > 0$ with 95% CI.

## E2 — Ten L2 States
**Goal:** Test H6.
**Data:** Controlled synthetic data.
**Criterion:** Correct response in ≥8 states.

## E3 — Failure Test
**Goal:** Test H5.
**Data:** Historical gaps.
**Criterion:** Recovery in <10 ticks.

## E4 — Conservation Test
**Goal:** Test H7.
**Data:** 100,000 ticks.
**Criterion:** $\|\phi\| < 10^{-6}$.

## E5 — Comparison with Classical A-S
**Goal:** Superiority of geometric mapping.
**Data:** Same data.
**Criterion:** Higher Sharpe.

## E6 — Cross-Timeframe Test
**Goal:** Compatibility at 1m, 5m, 1h.
**Criterion:** Orbit correlation > 0.7.

## E7 — Multidimensional Test
**Goal:** Three parallel timeframes.
**Criterion:** Synchronization without divergence.

## Statistical Design
- Paired t-test
- Bootstrap 10,000 samples
- Bonferroni correction $\alpha/n$
