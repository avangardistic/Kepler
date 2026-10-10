# OrderBookMath

## Total Potential
$$
\Phi(p) = -G \sum_i \sum_k \frac{q_k^i}{|p - p_k^i|}
$$

## Gradient (Force)
$$
F^\Phi(p) = -\frac{\partial \Phi}{\partial p} = -G \sum_i \sum_k \frac{q_k^i \cdot \text{sgn}(p - p_k^i)}{(p - p_k^i)^2}
$$

## Potential Wells
High-volume levels = deep wells.

## Lagrangian Points
Three bodies + book wells = L1..L5 points.

## Instability
Level with:
$$
\frac{\partial^2 \Phi}{\partial p^2} < 0
$$
is unstable and collapses.

## Linear Approximation
For $p \approx p_k$:
$$
\Phi(p) \approx -\frac{G q_k}{|p - p_k|} + \text{const}
$$

## Benford Test
First-digit distribution of volumes should be Benford:
$$
P(d) = \log_{10}(1 + 1/d)
$$
Deviation = manipulation.
