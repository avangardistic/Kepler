# TickModel

## Definition of tick
$$
\text{tick} = \text{one L2 update}
$$

## Consequences

1. **No fixed $\Delta t$ exists.** Integration step = tick.
2. **Velocity**:
$$
v_i = x_i(t) - x_i(t-1)
$$
3. **Symplectic integrator** on tick:
$$
\begin{aligned}
p^{n+1/2} &= p^n - \tfrac{1}{2}\nabla V(x^n) \\
x^{n+1}   &= x^n + p^{n+1/2}/m \\
p^{n+1}   &= p^{n+1/2} - \tfrac{1}{2}\nabla V(x^{n+1})
\end{aligned}
$$

## Timing and alignment
- Phase 1 ingests Binance `depth20@100ms` **snapshots** for BTC/ETH/SOL; each received update is one tick.
- Replay emits one three-body state per tick once all three assets have a book, using each asset's latest snapshot (latest-wins). Sequence gaps in `lastUpdateId` are normal for snapshot streams and are not counted as drops; only a regression is an ordering violation.
- No virtual-clock merging, interpolation, or cross-venue alignment is implemented: those would be derived data (Axiom 1). Coinbase and other venues are outside the current single-feed scope (Assumptions.md §5).
- Decision record: ADR-011 in [`../02_engineering/Decisions.md`](../02_engineering/Decisions.md).

## Effect on Physics
- Kinetic energy in discrete tick:
$$
T = \tfrac{1}{2}\sum m_i v_i^2
$$
- Angular momentum in discrete tick:
$$
\vec L = \sum m_i (\mathbf{x}_i \times \mathbf{v}_i)
$$

## Quantization
Each tick = one quantum of time. No divisibility.
