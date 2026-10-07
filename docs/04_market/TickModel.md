# TickModel

## تعریف tick
$$
\text{tick} = \text{یک به‌روزرسانی L2}
$$

## پیامدها

1. **هیچ $\Delta t$ ثابتی وجود ندارد.** گام انتگرال = tick.
2. **سرعت**:
$$
v_i = x_i(t) - x_i(t-1)
$$
3. **انتگرال‌گیر symplectic** روی tick:
$$
\begin{aligned}
p^{n+1/2} &= p^n - \tfrac{1}{2}\nabla V(x^n) \\
x^{n+1}   &= x^n + p^{n+1/2}/m \\
p^{n+1}   &= p^{n+1/2} - \tfrac{1}{2}\nabla V(x^{n+1})
\end{aligned}
$$

## زمان‌بندی
- Binance: هر ۱۰۰ms یا هر تغییر
- Coinbase: هر ۵۰ms
- نرمال‌سازی: ادغام به tick‌های ثابت مجازی

## اثر بر فیزیک
- انرژی جنبشی در tick گسسته:
$$
T = \tfrac{1}{2}\sum m_i v_i^2
$$
- مومنتوم زاویه‌ای در tick گسسته:
$$
\vec L = \sum m_i (\mathbf{x}_i \times \mathbf{v}_i)
$$

## کوانتش
هر tick = یک کوانتوم زمان. هیچ تقسیم‌پذیری ندارد.
