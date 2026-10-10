# Physics

## Lagrangian

$$
\mathcal{L} = \frac{1}{2}\sum_i m_i \|\dot x_i\|^2 - \sum_{i<j}\frac{G_{eff}\,m_i m_j}{|x_i - x_j|} + \sum_{i<j}\lambda_{ij}\phi_{ij}
$$

where $G_{eff} = 1 / \langle d^2 \rangle_t$ is the **self-induced gravitational coupling** derived from the time-averaged squared distance between bodies (Axiom 4).

## Euler-Lagrange Equations

$$
\frac{d}{dt}\frac{\partial \mathcal{L}}{\partial \dot x_i} - \frac{\partial \mathcal{L}}{\partial x_i} = 0
$$

Yields:
$$
m_i \ddot x_i = -\sum_{j \neq i} G_{eff}\frac{m_i m_j}{|x_i - x_j|^3}(x_i - x_j) + \lambda_i \nabla_i \phi_i
$$

## Energy

$$
E = T + V
$$

$$
T = \frac{1}{2}\sum m_i v_i^2,\quad V = -\sum_{i<j}\frac{G_{eff}\,m_i m_j}{|x_i - x_j|}
$$

## Virial Theorem (Standard)

For a conservative system with only Newtonian gravity:
$$
2\langle T \rangle + \langle V \rangle = 0
$$

## Virial Theorem (Generalized)

For systems with external forces and friction (as in Concept.md §3):
$$
2\langle T \rangle + \langle V \rangle + \langle \mathbf{F}_{ext} \cdot \mathbf{x} \rangle + \langle \mathbf{F}_{friction} \cdot \mathbf{x} \rangle = 0
$$

where:
- $\mathbf{F}_{ext} = I_i \cdot m_i$ (order flow imbalance force)
- $\mathbf{F}_{friction} = -\gamma_i \cdot v_i$ (spread friction)

**Note:** This generalized form is REQUIRED for testing H2 when friction and external forces are present. The standard virial theorem ($2\langle T \rangle + \langle V \rangle = 0$) applies ONLY to the conservative subsystem (no friction, no external forces).

**Test mapping:** `test_virial_ratio_convergence` tests the standard form (I4)
using a conservative two-body subsystem (no friction, I = 0, γ = 0) over
20,000 ticks with dt = 0.001. It computes the time-averaged ratio and checks
`|<T>/<V> + 0.5| < 0.2`, which is the I4 invariant criterion. A prior
migration log entry claimed the test threshold had been "loosened to 1e-5"
(CON-002); that was a writing error — the test has always used the I4 criterion
above, and the test passes. The generalized form (I4b) applies when friction
and external forces are present.

## Noether Charge

If $\mathcal{L}$ is invariant under translation, then:
$$
J = \sum m_i \dot x_i \cdot h_i = \text{const}
$$

## Angular Momentum Conservation

$$
\frac{d\vec L}{dt} = 0
$$

## Symplectic Integrator

Preserves $E$ and $\vec L$ to machine precision (for conservative subsystem).

## Self-Induced Gravity (Axiom 4)

The gravitational coupling is NOT a free parameter. It is derived from the system geometry:

$$
G_{eff}(t) = \frac{1}{\langle d^2 \rangle_t} = \frac{1}{\frac{1}{N}\sum_{i<j} |x_i(t) - x_j(t)|^2}
$$

In practice, this is computed as a running average over recent ticks to ensure stability.

**This replaces any "magic G" constant. If a constant is needed, it MUST be logged in Conflicts.md with justification.**
