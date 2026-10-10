# Detectors

## 1. Iceberg Detector

### Definition
An order that appears with small visible size, fills, then replenishes.

### Score
$$
\text{score}_\text{ice} = \text{refills} \cdot (1 - r_\text{visible}) \cdot \min(t/60, 1)
$$
where $r_\text{visible} = q_\text{now}/q_\text{peak}$.

### Thresholds
- refills ≥ 3
- $r_\text{visible} < 0.4$
- lifetime ≥ 5s

### Statistical Test
K-S on inter-refill times:
$$
D_n = \sup_x |F_n(x) - F_0(x)|
$$
If $D_n > c_\alpha/\sqrt{n}$ → iceberg.

## 2. Spoof Detector

### Definition
Large order far from mid that disappears quickly.

### Score
$$
\text{score}_\text{spoof} = z \cdot c_\text{ratio} \cdot e^{-d/100} \cdot \frac{1}{t+1} \cdot 100
$$
where:
- $z$: volume z-score
- $c_\text{ratio}$: cancel/fill ratio
- $d$: distance in bps from mid
- $t$: age (seconds)

### Thresholds
- $z > 3$
- $d > 5$ bps
- $t < 10$s
- fills = 0

## 3. Hawkes Test
Cancellation rate:
$$
\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta(t-t_i)}
$$
Clustering = spoof.

## 4. Survival Test
$$
S(t) = P(T > t)
$$
spoof: $S(t)$ drops quickly.
