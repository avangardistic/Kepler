# Microprice

## Standard Definition
$$
P^\mu = \frac{q_1^a \cdot p_1^b + q_1^b \cdot p_1^a}{q_1^a + q_1^b}
$$

## Properties
- If $q^b = q^a$: $P^\mu = \text{mid}$
- If bid-heavy ($q^b > q^a$): $P^\mu > \text{mid}$
- If ask-heavy: $P^\mu < \text{mid}$

## Advanced Variants

### Weighted Microprice
$$
P^\mu_W = \frac{\sum_k w_k q_k^a p_k^b + \sum_k w_k q_k^b p_k^a}{\sum_k w_k (q_k^a + q_k^b)}
$$
where $w_k = e^{-\alpha k}$.

### Volume-Weighted Mid
$$
P^\mu_V = \frac{\sum_k q_k^b p_k^b + \sum_k q_k^a p_k^a}{\sum_k (q_k^b + q_k^a)}
$$

## Selection in This Project
Standard $P^\mu$ is used because:
- Comes only from level 1
- Sensitive to immediate change
- No free parameter
