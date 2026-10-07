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

## Virial Theorem — Numerical Requirements (added 2026-10-07, R-PHY-001)
The identities above are statements about trajectories of the *continuous*
system with *constant* $G$. Empirically verified requirements for any test of
them (see `06_research/physics/virial_theorem.md` for full data):
1. **Dimensionality.** In 1-D every bound orbit is a radial plunge (L = 0,
   no centrifugal barrier); its close approach cannot be resolved at tick-like
   dt, so per-tick or partial-window "virial ratios" measure numerical heating,
   not physics (FailureModes F10). Circular orbits, where
   $T/V = -\frac12$ holds at every tick, exist only for configurations with
   $\|\vec L\| > 0$.
2. **Windowing.** $\langle T\rangle/\langle V\rangle = -\frac12 + O(\epsilon)$
   was measured at $\le 10^{-7}$ deviation for eccentricities up to e ≈ 0.75
   when averaging over exact integer Kepler periods; partial windows carry
   $O(10^{-2})$ bias.
3. **Precision.** float64 is required for the 1e−9-class conservation
   assertions (float32 ε ≈ 1.2e−7).
4. **Softening.** Isotropic: $d_\epsilon = \sqrt{\|\Delta x\|^2 + \epsilon^2}$
   on the full separation vector (engine fixed 2026-10-07; per-coordinate
   softening is not a central force and admits no circular orbit).

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

> **Implementation status note (2026-10-07 audit):** the engine currently
> computes $G_{eff}$ **once from the initial state and freezes it** for the
> trajectory (`integrate()`), which is a *different* dynamical system from the
> running-average reading above (only frozen G is Hamiltonian/conservative —
> see I2). The divergence, and the degenerate-geometry fallback `G = 1.0`
> (a magic constant in disguise), are tracked as **CON-003** and analyzed in
> `06_research/physics/gravity_derivation.md` (R-PHY-002). Do not "fix" either
> side before that decision is recorded here and in Decisions.md.

**This replaces any "magic G" constant. If a constant is needed, it MUST be logged in Conflicts.md with justification.**
