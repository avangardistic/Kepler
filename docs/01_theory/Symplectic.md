# Symplectic Integration

## 1. Why Symplectic?
Ordinary integrators (Euler, RK4) lose energy over time.
Symplectic preserves the geometric structure.

## 2. Störmer-Verlet
$$
\begin{aligned}
p^{n+1/2} &= p^n - \tfrac{\Delta t}{2}\nabla V(x^n) \\
x^{n+1}   &= x^n + \Delta t \cdot p^{n+1/2}/m \\
p^{n+1}   &= p^{n+1/2} - \tfrac{\Delta t}{2}\nabla V(x^{n+1})
\end{aligned}
$$

## 3. Properties
- Preserves $E$ to $O(\Delta t^2)$
- Preserves $\vec L$ to machine precision
- Time-reversible

## 4. Constraint Manifold Projection
After each step:
$$
(x, p) \leftarrow \text{Proj}_\Sigma(x, p)
$$

where $\Sigma = \phi^{-1}(0)$.

## 5. Error
$$
\Delta E \sim \Delta t^2 \cdot N_\text{tick}
$$

## 6. Comparison
| Method | Conservation |
|--------|----------|
| Euler | Poor |
| RK4 | Medium |
| Symplectic | Excellent |
| IMEX | Excellent + constraints |
