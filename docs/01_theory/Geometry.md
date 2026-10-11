# Geometry

> Exploratory notes on a proposed metric. Not implemented; the metric's `α` is
> a free parameter and would need a derivation before use (Axiom 4).

## Manifold
$$
\mathcal{M} = \{x = (x_1, x_2, x_3)\}
$$

## Metric
$$
g_{ij} = \delta_{ij} + \alpha \frac{\partial^2 \ln P}{\partial x_i \partial x_j}
$$

## Christoffel Symbols
$$
\Gamma^i_{jk} = \frac{1}{2}g^{i\ell}(\partial_j g_{k\ell} + \partial_k g_{j\ell} - \partial_\ell g_{jk})
$$

## Geodesic Equation
$$
\ddot x^i + \Gamma^i_{jk}\dot x^j \dot x^k = 0
$$

## Ricci Tensor
$$
\text{Ric}_{ij} = \partial_k \Gamma^k_{ij} - \partial_j \Gamma^k_{ik} + \Gamma^k_{k\ell}\Gamma^\ell_{ij} - \Gamma^k_{j\ell}\Gamma^\ell_{ik}
$$

## Scalar Curvature
$$
R = g^{ij}\text{Ric}_{ij}
$$

## Ricci Flow
$$
\frac{\partial g_{ij}}{\partial t} = -2\text{Ric}_{ij}
$$

## Application to Market
- Strong trend → high curvature → strong gravity
- Range → zero curvature → medium gravity
