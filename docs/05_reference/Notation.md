# Notation

## Symbols

| Symbol | Definition | Unit |
|------|--------|------|
| $i, j$ | Asset index (1,2,3) | — |
| $t$ | Tick number | — |
| $P_i$ | Price of asset i | USDT |
| $P_i^\mu$ | Microprice (see `../01_theory/Microprice.md`; implementation status is CON-011) | USDT |
| $x_i$ | Model position, $x_i = \ln P_i^\mu$ | — |
| $v_i$ | Orbital velocity | 1/tick |
| $p_i$ | Momentum | — |
| $m_i$ | Model mass, $m_i = \ln(1 + \text{depth})$ (not a measured physical mass) | — |
| $I_i$ | Imbalance | — |
| $\gamma_i$ | Friction | — |
| $q_k^{b,i}$ | Bid depth at level k | — |
| $q_k^{a,i}$ | Ask depth at level k | — |
| $G_{eff}$ | Self-induced coupling $1/\langle d^2 \rangle$ (not a free constant; Axiom 4) | — |
| $\vec L$ | Angular momentum | — |
| $\Pi$ | Proposed mathematical work functional (Axiom 7). Not profit or P&L | — |
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
- `ns` suffix (as in `ts_exchange_ns`): nanoseconds
- Subscript: coordinate (i=asset, k=level)
