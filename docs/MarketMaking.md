# Market Making

## 1. Classic Avellaneda-Stoikov Model

Reservation price:
$$
r(s,t) = s - q\gamma\sigma^2(T-t)
$$

Optimal spread:
$$
\delta_\pm = \gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln\!\Big(1 + \frac{\gamma}{k}\Big)
$$

## 2. Mapping to Three-Body

| A-S | Three-Body |
|-----|----------|
| $\gamma$ (risk aversion) | $1/\|\vec L\|$ |
| $q$ (inventory) | $m \cdot v$ |
| $s$ | $x_i$ |
| $\sigma^2$ | $\|F^\text{grav}\|/m$ |
| $k$ | constant (fill intensity) |

## 3. Final Formulas

Reservation:
$$
r_i = x_i - (m_i v_i) \cdot \frac{1}{\|\vec L\|} \cdot \frac{\|F_i^\text{grav}\|}{m_i} \cdot (T-t)
$$

Spread:
$$
\delta_i = \frac{\sigma_i^2}{\|\vec L\|}(T-t) + 2\|\vec L\|\ln\!\Big(1 + \frac{1}{k\|\vec L\|}\Big)
$$

## 4. Skew from Imbalance
$$
\text{skew}_i = \frac{1}{2}\cdot\frac{q_i^b - q_i^a}{q_i^b + q_i^a}
$$

## 5. Final Bid/Ask
$$
\text{Bid}_i = r_i - \delta_i/2 + \text{skew}_i
$$
$$
\text{Ask}_i = r_i + \delta_i/2 + \text{skew}_i
$$

## 6. Without Risk Management
$\gamma = 1/\|\vec L\|$ self-adjusts.
If $\|\vec L\| \to 0$, spread → ∞ → freeze.
