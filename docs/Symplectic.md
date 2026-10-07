# Symplectic Integration

## 1. چرا symplectic؟
انتگرال‌گیرهای معمولی (Euler, RK4) انرژی را به‌مرور از دست می‌دهند.
Symplectic ساختار هندسی را حفظ می‌کند.

## 2. Störmer-Verlet
$$
\begin{aligned}
p^{n+1/2} &= p^n - \tfrac{\Delta t}{2}\nabla V(x^n) \\
x^{n+1}   &= x^n + \Delta t \cdot p^{n+1/2}/m \\
p^{n+1}   &= p^{n+1/2} - \tfrac{\Delta t}{2}\nabla V(x^{n+1})
\end{aligned}
$$

## 3. خاصیت
- حفظ $E$ تا $O(\Delta t^2)$
- حفظ $\vec L$ تا دقت ماشین
- برگشت‌پذیر زمانی

## 4. تصویر روی منیفلد قید
پس از هر گام:
$$
(x, p) \leftarrow \text{Proj}_\Sigma(x, p)
$$

که $\Sigma = \phi^{-1}(0)$.

## 5. خطا
$$
\Delta E \sim \Delta t^2 \cdot N_\text{tick}
$$

## 6. مقایسه
| روش | پایستگی |
|------|----------|
| Euler | بد |
| RK4 | متوسط |
| Symplectic | عالی |
| IMEX | عالی + قید |
