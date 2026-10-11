# Microprice

> **Remark (open conflict CON-011).** The formulas below are the documented
> definition. The current `state_from_l2` implementation does **not** evaluate
> the standard level-1 microprice: it uses a sum over the received price levels
> (and applies `_gamma` to the log price instead of the price). See
> [`../03_research/Conflicts.md`](../03_research/Conflicts.md) CON-011 before
> relying on a measured `x_i`.

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

## Position mapping

The model position is `x_i = ln P^μ_i` (Concept.md §2.2); the implementation
status of that mapping is tracked in CON-011.
