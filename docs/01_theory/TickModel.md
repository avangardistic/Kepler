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

## Timing
- Binance: every 100ms or on every change
- Coinbase: every 50ms
- Normalization: merge into fixed virtual ticks

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
