# Notation

## Symbols

| Symbol | Definition | Unit |
|------|--------|------|
| $i, j$ | Asset index (1,2,3) | — |
| $t$ | Tick number | — |
| $P_i$ | Price of asset i | USDT |
| $P_i^\mu$ | Microprice | USDT |
| $x_i$ | Log microprice | — |
| $v_i$ | Orbital velocity | 1/tick |
| $p_i$ | Momentum | — |
| $m_i$ | Effective mass | — |
| $I_i$ | Imbalance | — |
| $\gamma_i$ | Friction | — |
| $q_k^{b,i}$ | Bid depth at level k | — |
| $q_k^{a,i}$ | Ask depth at level k | — |
| $G$ | Gravitational constant | 1.0 |
| $\vec L$ | Angular momentum | — |
| $\Pi$ | Cumulative profit | — |
| $\phi_{ij}$ | Hedge constraint | — |
| $\lambda_i$ | Lagrange multiplier | — |
| $T$ | Kinetic energy | — |
| $V$ | Potential energy | — |
| $\mathcal{V}$ | Virial ratio | — |

## Operators
- $\dot x = dx/dt$ derivative w.r.t. tick
- $\nabla_i$ gradient w.r.t. $x_i$
- $\langle \cdot \rangle$ time average
- $\|\cdot\|$ Euclidean norm

## Indices
- Superscript: type (b=bid, a=ask, eff=effective)
- Subscript: coordinate (i=asset, k=level)
