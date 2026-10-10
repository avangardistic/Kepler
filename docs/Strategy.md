# Strategy

## 1. Nature
Pure market making with geometric parameters. Always two-sided.

## 2. Tick Cycle
1. **Ingest:** Receive L2
2. **Measure:** Compute x, m, I, γ
3. **Evolve:** Symplectic step
4. **Quote:** Compute bid/ask

## 3. Quoting Rules

Reservation price:
$$
r_i = x_i - (m_i v_i) \cdot \frac{1}{\|\vec L\|} \cdot \frac{\|F_i^\text{grav}\|}{m_i} \cdot (T-t)
$$

Spread:
$$
\delta_i = \frac{\sigma_i^2}{\|\vec L\|}(T-t) + 2\|\vec L\|\ln\!\Big(1 + \frac{1}{k\|\vec L\|}\Big)
$$

Final:
$$
\text{Bid}_i = r_i - \tfrac{\delta_i}{2} + \text{skew}_i,\quad \text{Ask}_i = r_i + \tfrac{\delta_i}{2} + \text{skew}_i
$$

## 4. Volume
$$
Q_i = \kappa \cdot m_i^{\text{eff}} \cdot \frac{1}{1 + \|\vec L\|}
$$

## 5. Automatic Hedge
Hedge = mass ratio. No separate layer.

## 6. Success Criteria
- ‖L‖ bounded
- Virial ratio → -1/2
- Π > 0 in mathematical expectation
- Max Drawdown zero (self-freeze)

## 7. Anti-Strategy
❌ Price prediction, signals, stop-loss, time-frame.
