# Concept

## 1. Big Picture
Three assets (BTC, ETH, SOL) as three gravitational bodies in log-microprice space.
Time advances by **tick**.

## 2. Fundamental Quantities

### 2.1 Raw Input
$$
\text{Tick}_t = \big\{\, \text{Bids}_t^i,\ \text{Asks}_t^i \,\big\}_{i=1}^{3}
$$

### 2.2 Orbital Position
$$
x_i(t) = \ln P_i^\mu(t)
$$
$$
P_i^\mu = \frac{q_1^a\,p_1^b + q_1^b\,p_1^a}{q_1^a + q_1^b}
$$

### 2.3 Mass
$$
m_i(t) = \ln\!\Big(1 + \sum_k q_k^{b,i} + \sum_k q_k^{a,i}\Big)
$$

### 2.4 Imbalance
$$
I_i(t) = \frac{\sum_k q_k^{b,i} - \sum_k q_k^{a,i}}{\sum_k q_k^{b,i} + \sum_k q_k^{a,i}}
$$

### 2.5 Friction
$$
\gamma_i(t) = \frac{p_1^{a,i} - p_1^{b,i}}{P_i^\mu(t)}
$$

## 3. Equation of Motion
$$
m_i \ddot x_i = -\sum_{j \neq i} G\,\frac{m_i m_j}{|x_i - x_j|^3}(x_i - x_j) + I_i \cdot m_i - \gamma_i \dot x_i
$$

## 4. Order Book Potential
$$
\Phi_i(p) = -\sum_k \frac{G\,q_k^{b,i}}{|p - p_k^{b,i}|} - \sum_k \frac{G\,q_k^{a,i}}{|p - p_k^{a,i}|}
$$

## 5. Hedge Constraint
$$
h_{ij} = \frac{m_j \cdot |I_i|}{m_i \cdot |I_j| + m_j \cdot |I_i|}
$$

## 6. Grid on L2
Grid levels = actual order book levels.

## 7. Angular Momentum
$$
\vec L = \sum_{i=1}^{3} m_i\,(\mathbf{x}_i \times \mathbf{v}_i)
$$

## 8. Profit
$$
\Pi = \iint_A \vec L\, dA
$$

## 9. Ten L2 States
Balanced, Bid-heavy, Ask-heavy, Thin, Thick, Spoof, Iceberg, Sweep, Flash, Squeeze.
