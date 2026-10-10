# Hedge Mathematics

## 1. Hedge Ratio
$$
h_{ij} = \frac{m_j |I_i|}{m_i |I_j| + m_j |I_i|}
$$

## 2. Holonomic Constraint
$$
\phi_{ij}(h) = h_{ij} - \frac{m_j |I_i|}{m_i |I_j| + m_j |I_i|} = 0
$$

## 3. Lagrange Multiplier
$$
\lambda_i = -\frac{\langle \nabla_i \phi, F_i^\text{net}\rangle}{\|\nabla_i \phi\|^2}
$$

## 4. Constraint Force
$$
F_i^\text{hedge} = \lambda_i \nabla_i \phi
$$

## 5. Constraint Tensor
$$
\Phi = \begin{pmatrix} 0 & \phi_{12} & \phi_{13} \\ -\phi_{12} & 0 & \phi_{23} \\ -\phi_{13} & -\phi_{23} & 0 \end{pmatrix}
$$

## 6. Manifold Projection
$$
x^\star = x - \Phi^\top (\Phi \Phi^\top)^{-1} \phi(x)
$$

## 7. Noether Conservation
If $\mathcal{L}$ is invariant under $h$:
$$
J = \sum m_i \dot x_i \cdot h_i = \text{const}
$$

## 8. Application
Hedge = automatic mass ratio. No manual decision.
