# OrderBookMath

## پتانسیل کل
$$
\Phi(p) = -G \sum_i \sum_k \frac{q_k^i}{|p - p_k^i|}
$$

## گرادیان (نیرو)
$$
F^\Phi(p) = -\frac{\partial \Phi}{\partial p} = -G \sum_i \sum_k \frac{q_k^i \cdot \text{sgn}(p - p_k^i)}{(p - p_k^i)^2}
$$

## چاه‌های پتانسیل
سطوح با حجم بالا = چاه عمیق.

## نقاط لاگرانژی
سه جسم + چاه‌های دفتر = نقاط L1..L5.

## ناپایداری
سطح با:
$$
\frac{\partial^2 \Phi}{\partial p^2} < 0
$$
ناپایدار است و شکسته می‌شود.

## تقریب خطی
برای $p \approx p_k$:
$$
\Phi(p) \approx -\frac{G q_k}{|p - p_k|} + \text{const}
$$

## آزمون بنفورد
توزیع رقم اول حجم‌ها باید Benford باشد:
$$
P(d) = \log_{10}(1 + 1/d)
$$
انحراف = دستکاری.
