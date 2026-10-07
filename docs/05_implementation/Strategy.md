# Strategy

## 1. ماهیت
Market Making خالص با پارامترهای هندسی. همیشه دو طرفه.

## 2. چرخه tick
1. **Ingest:** دریافت L2
2. **Measure:** محاسبه x, m, I, γ
3. **Evolve:** گام سیمپلکتیک
4. **Quote:** محاسبه bid/ask

## 3. قواعد کوتیشن

قیمت رزرو:
$$
r_i = x_i - (m_i v_i) \cdot \frac{1}{\|\vec L\|} \cdot \frac{\|F_i^\text{grav}\|}{m_i} \cdot (T-t)
$$

اسپرد:
$$
\delta_i = \frac{\sigma_i^2}{\|\vec L\|}(T-t) + 2\|\vec L\|\ln\!\Big(1 + \frac{1}{k\|\vec L\|}\Big)
$$

نهایی:
$$
\text{Bid}_i = r_i - \tfrac{\delta_i}{2} + \text{skew}_i,\quad \text{Ask}_i = r_i + \tfrac{\delta_i}{2} + \text{skew}_i
$$

## 4. حجم
$$
Q_i = \kappa \cdot m_i^{\text{eff}} \cdot \frac{1}{1 + \|\vec L\|}
$$

## 5. هج خودکار
هج = نسبت جرم. هیچ لایه جداگانه.

## 6. معیارهای موفقیت
- ‖L‖ کران‌دار
- نسبت ویریال به -1/2
- Π > 0 در امید ریاضی
- Max Drawdown صفر (فریز خودکار)

## 7. ضد-استراتژی
❌ پیش‌بینی قیمت، سیگنال، حد ضرر، تایم‌فریم.
