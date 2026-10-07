# Market Making

## 1. مدل آولاندا-استویکوف کلاسیک

قیمت رزرو:
$$
r(s,t) = s - q\gamma\sigma^2(T-t)
$$

اسپرد بهینه:
$$
\delta_\pm = \gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln\!\Big(1 + \frac{\gamma}{k}\Big)
$$

## 2. نگاشت به سه‌جسمی

| A-S | سه‌جسمی |
|-----|---------|
| $\gamma$ (ریسک) | $1/\|\vec L\|$ |
| $q$ (inventory) | $m \cdot v$ |
| $s$ | $x_i$ |
| $\sigma^2$ | $\|F^\text{grav}\|/m$ |
| $k$ | ثابت (شدت پر شدن) |

## 3. فرمول نهایی

رزرو:
$$
r_i = x_i - (m_i v_i) \cdot \frac{1}{\|\vec L\|} \cdot \frac{\|F_i^\text{grav}\|}{m_i} \cdot (T-t)
$$

اسپرد:
$$
\delta_i = \frac{\sigma_i^2}{\|\vec L\|}(T-t) + 2\|\vec L\|\ln\!\Big(1 + \frac{1}{k\|\vec L\|}\Big)
$$

## 4. Skew از عدم توازن
$$
\text{skew}_i = \frac{1}{2}\cdot\frac{q_i^b - q_i^a}{q_i^b + q_i^a}
$$

## 5. Bid/Ask نهایی
$$
\text{Bid}_i = r_i - \delta_i/2 + \text{skew}_i
$$
$$
\text{Ask}_i = r_i + \delta_i/2 + \text{skew}_i
$$

## 6. بدون مدیریت ریسک
$\gamma = 1/\|\vec L\|$ خودبه‌خود تنظیم می‌شود.
اگر $\|\vec L\| \to 0$، اسپرد → ∞ → فریز.
