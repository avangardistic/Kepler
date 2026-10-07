# Roadmap

> **اصل تغییرناپذیر:** هیچ مدیریت ریسکی، فیلتری، اندیکاتوری، پارامتر بیرونی.

## فاز 0: پایه نظری ✅
- Philosophy, Concept, Strategy, Implementation, Notation, Glossary

## فاز 1: زیرساخت Tick
- DataSpec, TickModel, fast_l2_client, tick_buffer, replay
- معیار خروج: ۱۰۰٬۰۰۰ tick بدون افت

## فاز 2: فیزیک
- Physics, physics_jax, Invariants
- معیار خروج: ‖L‖ کران‌دار در ۹۰٪ زمان

## فاز 3: تشخیص‌ها
- Detectors, detectors_numba, K-S test
- معیار خروج: F1 > 0.8

## فاز 4: Market Making
- MarketMaking, market_maker
- معیار خروج: اسپرد همیشه مثبت

## فاز 5: شبیه‌سازی
- ۱۰ میلیون tick
- معیار خروج: Π > 0 با CI 95%

## فاز 6: اعتبارسنجی
- Hypotheses, Experiments, t-test, bootstrap
- معیار خروج: رد/تأیید فرضیه اصلی

## فاز 7: بسط ریاضی
- هندسه دیفرانسیل، ریچی، گیج، کوانتش

## فاز 8: چندجهانی
- JAX vmap روی ۳ تایم‌فریم

## فاز 9: مستندسازی نهایی
- References, OpenProblems, whitepaper

## فاز 10: نظریه واحد
- Orbit ↔ Profit ↔ Information

## جدول زمانی
| فاز | مدت |
|-----|------|
| 0 | ✅ |
| 1 | 2 هفته |
| 2 | 3 هفته |
| 3 | 2 هفته |
| 4 | 2 هفته |
| 5 | 4 هفته |
| 6 | 2 هفته |
| 7 | 6 هفته |
| 8 | 3 هفته |
| 9 | 2 هفته |
