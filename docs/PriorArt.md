# Prior Art

## مدل‌های فیزیکی بازار
- **Econophysics** (Stanley, Mantegna): توزیع‌های توانی در بازده.
- **Ising model** (Bornholdt): فاز انتقال در بازار.
- **Coupled oscillators** (Sornette): نوسان‌های همگام.

## مدل‌های سه‌جسمی در مالی
- **Triangular arbitrage** به‌عنوان سه‌جسمی (Zhou et al.)
- **Cross-currency dynamics** با معادلات Lotka-Volterra.
- **Network triplets** (Aste).

## Market Making مدرن
- **A-S (2008)** با inventory risk.
- **Guéant-Lehalle-Fernandez-Tapia (2013)** با محدودیت.
- **Cartea-Jaimungal** با تابع ارزش.

## تفاوت این پروژه
1. ترکیب **سه‌جسمی + market making + L2**.
2. **بدون مدیریت ریسک**: ریسک در قید هندسی.
3. **بدون فیلتر**: تطبیق خودزا.
4. **tick-based**: کوانتش زمان.
5. **بازی ریاضی**: هرگز اجرا نمی‌شود.

## چه چیز جدید است؟
- نگاشت A-S به سه‌جسمی از طریق $\gamma = 1/\|\vec L\|$.
- هج = نسبت جرم (نه تصمیم).
- گرید = سطوح واقعی L2 (نه فاصله محاسباتی).
- فریز خودکار در $\|\vec L\| = 0$.
