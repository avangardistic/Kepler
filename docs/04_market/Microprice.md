# Microprice

## تعریف استاندارد
$$
P^\mu = \frac{q_1^a \cdot p_1^b + q_1^b \cdot p_1^a}{q_1^a + q_1^b}
$$

## خواص
- اگر $q^b = q^a$: $P^\mu = \text{mid}$
- اگر bid-heavy ($q^b > q^a$): $P^\mu > \text{mid}$
- اگر ask-heavy: $P^\mu < \text{mid}$

## انواع پیشرفته

### Weighted Microprice
$$
P^\mu_W = \frac{\sum_k w_k q_k^a p_k^b + \sum_k w_k q_k^b p_k^a}{\sum_k w_k (q_k^a + q_k^b)}
$$
که $w_k = e^{-\alpha k}$.

### Volume-Weighted Mid
$$
P^\mu_V = \frac{\sum_k q_k^b p_k^b + \sum_k q_k^a p_k^a}{\sum_k (q_k^b + q_k^a)}
$$

## انتخاب در این پروژه
از $P^\mu$ استاندارد استفاده می‌شود چون:
- تنها از سطح ۱ می‌آید
- حساس به تغییر فوری
- بدون پارامتر آزاد
