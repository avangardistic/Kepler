# Detectors

## 1. Iceberg Detector

### تعریف
سفارشی که با حجم visible کوچک ظاهر می‌شود، پر می‌شود، دوباره پر می‌شود.

### امتیاز
$$
\text{score}_\text{ice} = \text{refills} \cdot (1 - r_\text{visible}) \cdot \min(t/60, 1)
$$
که $r_\text{visible} = q_\text{now}/q_\text{peak}$.

### آستانه
- refills ≥ 3
- $r_\text{visible} < 0.4$
- lifetime ≥ 5s

### آزمون آماری
K-S روی inter-refill times:
$$
D_n = \sup_x |F_n(x) - F_0(x)|
$$
اگر $D_n > c_\alpha/\sqrt{n}$ → iceberg.

## 2. Spoof Detector

### تعریف
سفارش بزرگ دور از mid که به‌سرعت ناپدید می‌شود.

### امتیاز
$$
\text{score}_\text{spoof} = z \cdot c_\text{ratio} \cdot e^{-d/100} \cdot \frac{1}{t+1} \cdot 100
$$
که:
- $z$: z-score حجم
- $c_\text{ratio}$: نسبت cancel/fill
- $d$: فاصله bps از mid
- $t$: عمر (ثانیه)

### آستانه
- $z > 3$
- $d > 5$ bps
- $t < 10$s
- fills = 0

## 3. آزمون Hawkes
نرخ لغو:
$$
\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta(t-t_i)}
$$
خوشه‌بندی = spoof.

## 4. آزمون بقا
$$
S(t) = P(T > t)
$$
spoof: $S(t)$ سریع افت می‌کند.
