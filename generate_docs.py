#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_docs.py — Kepler documentation generator / snapshotter.

Writes every file below docs/ from the DOCS dict. Since the
2026-10-07 reorganization, docs/ is a 12-category nested tree and
this file embeds its full contents (regenerated from docs/ then).
Workflow: edit docs/ directly during a session, then refresh this
file so regeneration reproduces the tree, e.g.:
    python generate_docs.py --out /tmp/docs_check \
      && diff -r docs /tmp/docs_check --exclude=.git   # must be empty
Or rebuild from docs/ with the Session-2 helper pattern
(scan docs/**/*.md -> DOCS).  The docs themselves remain the working
truth during research; this generator guarantees reproducibility.

Original (Phase 0, 2025-01) generated Persian docs flat; Session 1
(2026-10-07) translated most to English; Session 2 (2026-10-07)
reorganized + resynced this file. Two legacy Persian docs are kept
verbatim (06_research/open_problems.md, 11_meta/goal.md,
12_prompts/master_prompt.md).
"""

import argparse
from datetime import datetime
from pathlib import Path

DOCS = {}


DOCS["00_INDEX.md"] = r"""# Kepler Documentation Index

> **The ONE file every agent reads first.** Last updated: 2026-10-07 (Session 2).

## What is Kepler?
A mathematical game exploring whether three-body orbital geometry can
describe Level-2 market microstructure. **NOT a trading system.** No capital,
no claims of profit, never run in production (see `01_foundation/Philosophy.md`).

## Current Status (verify, don't trust)
```bash
python -m pytest tests/ -v      # expected: 9 passed (requires jax, pytest; see STATE_INVENTORY)
```
- Test status: **9/9 passing** since 2026-10-07 (Session 2).
- Open conflicts: **none** (CON-001, CON-002 resolved).
- Failing-mode log: `08_failures/FailureModes.md` (F1–F10).

## Quick Navigation

### I need to understand the project
→ Read: `01_foundation/Philosophy.md` (5 min)
→ Read: `01_foundation/Axioms.md` (3 min)
→ Read: `02_concept/Concept.md` (10 min)

### I need to run the code
→ Read: `STATE_INVENTORY.md` (environment: float64 via `tests/conftest.py`, `pip install "jax[cpu]" pytest`)
→ Run: `python -m pytest tests/ -v`

### I need to know current state
→ Read: `docs/STATE_INVENTORY.md`
→ Read: `docs/ResearchLog.md` (top entry)
→ Read: `09_agents/AgentSync.md` (last 3 entries)

### I need to continue research
→ Read: `06_research/README.md` (topic registry + status)
→ Read: `07_hypotheses/Hypotheses.md`
→ Read: `08_failures/FailureModes.md`

### I need to fix a bug
→ Read: `08_failures/FailureModes.md` first — it may already be logged
→ Use: `10_templates/Five_Whys_Template.md`
→ QA rules: `09_agents/QA_Protocol.md` (P3: never loosen thresholds)

### I need to coordinate with other agents
→ Read: `09_agents/AgentSync.md`, `09_agents/AI_Protocol.md`
→ Leave a packet in: `09_agents/AgentHandoff.md` (top)

## Folder Map

| Folder | Purpose | When to Read |
|--------|---------|--------------|
| `00_INDEX.md` (this file) | Entry point, status, map | Every session start |
| `STATE_INVENTORY.md` (root) | Measured current state | Every session, before + after |
| `ResearchLog.md` (root) | Chronological research log | Append per session |
| `01_foundation/` | Philosophy, Axioms, Assumptions, Limitations — non-negotiable rules | First time only |
| `02_concept/` | Concept, Notation, Glossary | First time only |
| `03_physics/` | Physics, OrderBookMath, Geometry, Differential, GaugeTheory, Quantum, Symplectic, HedgeMath | When working on physics |
| `04_market/` | DataSpec, TickModel, Microprice, MarketMaking, Detectors, RegimeCatalog | When working on detectors/data |
| `05_implementation/` | Implementation, Strategy, roadmap | When writing code |
| `06_research/` | ACTIVE research only, one file per topic (R-XXX-###) | Every session |
| `07_hypotheses/` | Hypotheses, Experiments, Invariants, Falsifiability | Before any experiment |
| `08_failures/` | FailureModes (F1–F10), Conflicts (CON-###) | Every session |
| `09_agents/` | AgentSync, AgentHandoff, AI_Protocol, QA_Protocol, Paperclip_Coordination | Every session |
| `10_templates/` | Five_Whys_Template, FMEA_Template | As needed |
| `11_meta/` | Decisions (ADR), Changelog, References, PriorArt, goal, Project_History | Weekly review |
| `12_prompts/` | PromptLibrary, TaskQueue (T-###), master_prompt | Session start |

> Legacy note: `11_meta/goal.md` and `12_prompts/master_prompt.md` are original
> Persian artifacts kept verbatim; most other docs were translated to English in
> earlier sessions. Do not treat untranslated legacy files as current state.

> Docs are also MACHINE-GENERATED: `python generate_docs.py` rewrites every
> file in this tree from `generate_docs.py` (DOCS dict ↔ docs/ are kept in
> sync — if you edit docs, regenerate or update the generator, or CI drift
> wins). Check with:
> `python generate_docs.py --out /tmp/docs_check && diff -r docs /tmp/docs_check --exclude=.git`

## The Golden Rule
> Read `docs/STATE_INVENTORY.md` and `docs/09_agents/AgentSync.md`
> BEFORE any action. Update them AFTER any action.
> Never trust a session brief, a chat message, or a memory of test status —
> run `pytest` and record what you measure. (Session 2 audit found three
> inherited claims were false; see `ResearchLog.md`.)
"""

DOCS["01_foundation/Assumptions.md"] = r"""# Assumptions

## فرض‌های صریح

1. **پیوستگی L2**: دفتر همیشه حداقل ۲۰ سطح دارد.
2. **عدم تاخیر شبکه**: تأخیر < ۵ms (در شبیه‌سازی صفر).
3. **عدم همبستگی خارجی**: تنها سه ارز مورد بررسی.
4. **عدم دستکاری کلان**: بدون دخالت بانک مرکزی.
5. **میکروپریس معتبر**: بازتاب واقعی فشار خرید/فروش.
6. **عدم گپ اطلاعاتی**: هر tick در دسترس است.
7. **ثبات کارمزد**: کارمزد ثابت در طول اجرا.
8. **عدم محدودیت پوزیشن**: capacity بی‌نهایت.
9. **عدم اثر بازار**: کوتیشن‌ها قیمت را تغییر نمی‌دهند.
10. **عدم ورشکستگی صرافی**: ریسک طرف مقابل صفر.

## مرزهای اعتبار
خارج از این فرض‌ها، مدل اعتبار ندارد.
"""

DOCS["01_foundation/Axioms.md"] = r"""# Axioms

## اصل ۱ — واقعیت خام
تنها داده مجاز: L2 tick. هیچ داده مشتق‌شده.

## اصل ۲ — کوانتش زمان
زمان گسسته است. واحد = tick.

## اصل ۳ — جرم از حجم
$m_i = \ln(1 + D_i)$ تنها منبع جرم.

## اصل ۴ — گرانش خودزا
$\kappa_{ij} \propto m_i m_j / d^2$ بدون پارامتر آزاد.

## اصل ۵ — قید هج
هج از نسبت جرم، نه از تصمیم.

## اصل ۶ — بدون مدیریت ریسک
ریسک در هندسه حل شده.

## اصل ۷ — سود = کار
$\Pi = \oint p \cdot dx$.

## اصل ۸ — پایداری ویریال
سیستم به $T/V = -1/2$ میل می‌کند.

## اصل ۹ — رد‌پذیری
هر فرضیه معیار رد دارد.

## اصل ۱۰ — عدم اجرا
این پروژه هرگز معامله نمی‌کند.
"""

DOCS["01_foundation/Limitations.md"] = r"""# Limitations

## محدودیت‌های بنیادین

1. **کوری به اخبار**: سیستم فقط L2 می‌بیند.
2. **عدم آگاهی از رژیم کلان**: هیچ مکانیزم ماکرو ندارد.
3. **حساسیت به گپ**: در گپ بدون حجم، فریز می‌شود.
4. **عدم قابلیت multi-venue**: تک‌صرافی در MVP.
5. **محدودیت خطی‌سازی**: گرانش نیوتنی برای فاصله‌های بزرگ نادرست.
6. **عدم مدل‌سازی همبستگی منفی**: فقط جاذبه داریم، نه دافعه.
7. **عدم اثر حجم خودمان**: اگر اجرا شود، بازار را تغییر می‌دهد.

## چه چیزهایی سیستم نمی‌تواند ببیند
- اخبار
- تراکنش‌های on-chain
- جریان‌های OTC
- رفتار نهنگ‌ها در صرافی‌های دیگر
- تصمیمات فدرال
"""

DOCS["01_foundation/Philosophy.md"] = r"""# Philosophy

## 1. ماهیت پروژه
این پروژه یک **بازی ریاضی** است، نه یک سیستم معاملاتی.
هدف: آزمون اینکه آیا هندسه سه‌جسمی می‌تواند زبان توصیفی میکروساختار بازار در سطح tick باشد.

**هرگز اجرا نخواهد شد.** هیچ سرمایه‌ای درگیر نیست. هیچ ادعای سودی وجود ندارد.

## 2. اصول بنیادین

### 2.1 هیچ اندیکاتوری مجاز نیست
اندیکاتورها گذشته را فشرده می‌کنند و اطلاعات را از بین می‌برند.
سیستم فقط با داده خام L2 و tick کار می‌کند.

### 2.2 هیچ فیلتری مجاز نیست
مدار خودش فیلتر است. گرانش خودش اندیکاتور است.

### 2.3 هیچ مدیریت ریسکی وجود ندارد
مدیریت ریسک = اعتراف به اینکه مدل اشتباه است.
اگر هندسه درست باشد، ریسک در قید مدار حل می‌شود.

### 2.4 زمان کوانتیده است
واحد زمان = **یک tick**.

### 2.5 بازار یک میدان است، نه یک سری
قیمت یک نقطه در فضا نیست؛ جسم غوطه‌ور در میدان پتانسیل دفتر سفارش است.

## 3. اصل تطبیق خودزا
> سیستم باید بدون هیچ پارامتر بیرونی، خودش را با هر رژیم بازار تطبیق دهد.

| پارامتر | منبع درونی |
|---------|-----------|
| جرم | عمق L2 |
| فاصله | اختلاف میکروپریس |
| نیرو | عدم توازن bid/ask |
| اصطکاک | اسپرد |
| گرید | شعاع انحنا |
| هج | نسبت جرم |
| زمان | tick |

## 4. ماهیت بازی
- آیا سه جسم در میدان L2 مدار پایدار دارند؟
- آیا مومنتوم زاویه‌ای کران‌دار است؟
- آیا نسبت ویریال به -1/2 میل می‌کند؟
- آیا سود = انحنای مدار؟

## 5. ضد-اصول
- ❌ ربات معامله‌گر
- ❌ سیستم سیگنال‌دهی
- ❌ استراتژی قابل فروش
- ❌ مدل پیش‌بینی قیمت
- ✅ یک بازی ریاضی روی داده واقعی

## 6. اصل falsifiability
سیستم در سه حالت شکست می‌خورد:
1. گپ ناگهانی بدون حجم
2. L2 خالی (jump-to-zero depth)
3. درهم‌تنیدگی خارجی (اخبار کلان)
"""

DOCS["02_concept/Concept.md"] = r"""# Concept

## 1. تصویر بزرگ
سه ارز (BTC, ETH, SOL) به‌عنوان سه جسم گرانشی در فضای لگاریتم میکروپریس.
زمان با **tick** جلو می‌رود.

## 2. کمیت‌های بنیادی

### 2.1 ورودی خام
$$
\text{Tick}_t = \big\{\, \text{Bids}_t^i,\ \text{Asks}_t^i \,\big\}_{i=1}^{3}
$$

### 2.2 موقعیت مداری
$$
x_i(t) = \ln P_i^\mu(t)
$$
$$
P_i^\mu = \frac{q_1^a\,p_1^b + q_1^b\,p_1^a}{q_1^a + q_1^b}
$$

### 2.3 جرم
$$
m_i(t) = \ln\!\Big(1 + \sum_k q_k^{b,i} + \sum_k q_k^{a,i}\Big)
$$

### 2.4 عدم توازن
$$
I_i(t) = \frac{\sum_k q_k^{b,i} - \sum_k q_k^{a,i}}{\sum_k q_k^{b,i} + \sum_k q_k^{a,i}}
$$

### 2.5 اصطکاک
$$
\gamma_i(t) = \frac{p_1^{a,i} - p_1^{b,i}}{P_i^\mu(t)}
$$

## 3. معادله حرکت
$$
m_i \ddot x_i = -\sum_{j \neq i} G\,\frac{m_i m_j}{|x_i - x_j|^3}(x_i - x_j) + I_i \cdot m_i - \gamma_i \dot x_i
$$

## 4. پتانسیل دفتر
$$
\Phi_i(p) = -\sum_k \frac{G\,q_k^{b,i}}{|p - p_k^{b,i}|} - \sum_k \frac{G\,q_k^{a,i}}{|p - p_k^{a,i}|}
$$

## 5. قید هج
$$
h_{ij} = \frac{m_j \cdot |I_i|}{m_i \cdot |I_j| + m_j \cdot |I_i|}
$$

## 6. گرید روی L2
سطوح گرید = سطوح واقعی دفتر.

## 7. مومنتوم زاویه‌ای
$$
\vec L = \sum_{i=1}^{3} m_i\,(\mathbf{x}_i \times \mathbf{v}_i)
$$

## 8. سود
$$
\Pi = \iint_A \vec L\, dA
$$

## 9. ده حالت L2
Balanced, Bid-heavy, Ask-heavy, Thin, Thick, Spoof, Iceberg, Sweep, Flash, Squeeze.
"""

DOCS["02_concept/Glossary.md"] = r"""# Glossary

**Tick**: کوچک‌ترین واحد زمان. یک به‌روزرسانی L2.

**Level 2 (L2)**: دفتر سفارش با عمق چند سطح.

**Microprice**: میانگین وزنی best bid/ask با حجم.

**Imbalance**: تفاضل نرمالیزه bid/ask depth.

**Iceberg**: سفارش پنهان که به‌صورت مکرر پر می‌شود.

**Spoof**: سفارش بزرگ کاذب که بدون اجرا ناپدید می‌شود.

**Orbit**: مسیر سه جسم در فضای $(\ln P, m, I)$.

**Angular Momentum ($\vec L$)**: اندازه چرخش مدار.

**Virial Ratio**: نسبت T/V که به -1/2 میل می‌کند.

**Symplectic**: انتگرال‌گیر حفظ‌کننده انرژی.

**Hedge Constraint**: قید نسبت جرم بین سه ارز.

**Effective Mass**: جرم تصحیح‌شده با iceberg/spoof.

**Spoof Score**: امتیاز kاذب بودن یک سطح.

**Iceberg Score**: امتیاز پنهان بودن یک سطح.
"""

DOCS["02_concept/Notation.md"] = r"""# Notation

## نمادها

| نماد | تعریف | واحد |
|------|--------|------|
| $i, j$ | اندیس ارز (1,2,3) | — |
| $t$ | شماره tick | — |
| $P_i$ | قیمت ارز i | USDT |
| $P_i^\mu$ | میکروپریس | USDT |
| $x_i$ | لگاریتم میکروپریس | — |
| $v_i$ | سرعت مداری | ۱/tick |
| $p_i$ | مومنتوم | — |
| $m_i$ | جرم مؤثر | — |
| $I_i$ | عدم توازن | — |
| $\gamma_i$ | اصطکاک | — |
| $q_k^{b,i}$ | حجم bid سطح k | — |
| $q_k^{a,i}$ | حجم ask سطح k | — |
| $G$ | ثابت گرانش | 1.0 |
| $\vec L$ | مومنتوم زاویه‌ای | — |
| $\Pi$ | سود تجمعی | — |
| $\phi_{ij}$ | قید هج | — |
| $\lambda_i$ | ضریب لاگرانژ | — |
| $T$ | انرژی جنبشی | — |
| $V$ | انرژی پتانسیل | — |
| $\mathcal{V}$ | نسبت ویریال | — |

## عملگرها
- $\dot x = dx/dt$ مشتق نسبت به tick
- $\nabla_i$ گرادیان نسبت به $x_i$
- $\langle \cdot \rangle$ میانگین زمانی
- $\|\cdot\|$ نرم اقلیدسی

## اندیس‌ها
- بالا: نوع (b=bid, a=ask, eff=effective)
- پایین: مختصات (i=ارز, k=سطح)
"""

DOCS["03_physics/Differential.md"] = r"""# Differential Geometry Extensions

## 1. جریان ریچی تطبیقی
$$
\frac{\partial g_{ij}}{\partial t} = -2\text{Ric}_{ij} + 2\lambda(t) g_{ij}
$$

## 2. انتخاب $\lambda(t)$
$$
\lambda(t) = \alpha \cdot \|F^\text{grav}(t)\|
$$

## 3. اثر بر متریک
- روند: ریچی > 0 → انقباض → گرانش قوی
- آشوب: ریچی < 0 → انبساط → گرانش ضعیف

## 4. هولونومی
اگر انحنای کانکس صفر باشد، هولونومی بدیهی است.

## 5. کلاف مماس
$$
T\mathcal{M} = \bigcup_{x \in \mathcal{M}} T_x\mathcal{M}
$$

## 6. کانکس
$$
\nabla_X Y = X^i \partial_i Y^k \partial_k + X^i Y^j \Gamma^k_{ij} \partial_k
$$

## 7. کاربرد در هج
هج = جابه‌جایی موازی روی منیفلد.
"""

DOCS["03_physics/GaugeTheory.md"] = r"""# Gauge Theory for Gaps

## 1. میدان گیجی
$$
A_\mu = (\Phi, \mathbf{A})
$$

## 2. تبدیل گیجی
$$
x_i \to e^{i\theta_i} x_i
$$

## 3. زاویه چرخش
$$
\theta = \arctan\!\left(\frac{\sum m_i (\mathbf{x}_i \times \mathbf{v}_i)}{\sum m_i (\mathbf{x}_i \cdot \mathbf{v}_i)}\right)
$$

## 4. حفظ مومنتوم زاویه‌ای
$$
L = \sum m_i (\mathbf{x}_i \times \mathbf{v}_i) = \text{const}
$$

## 5. انحنا
$$
F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu
$$

## 6. کاربرد در گپ
در گپ صعودی: $\theta > 0$ → چرخش پوزیشن‌ها به سمت ارزهای دیگر.

## 7. شرط پایداری
$$
\frac{\partial^2 \Pi}{\partial \theta^2}\bigg|_{\theta^\star} < 0
$$
"""

DOCS["03_physics/Geometry.md"] = r"""# Geometry

## منیفلد
$$
\mathcal{M} = \{x = (x_1, x_2, x_3)\}
$$

## متریک
$$
g_{ij} = \delta_{ij} + \alpha \frac{\partial^2 \ln P}{\partial x_i \partial x_j}
$$

## نمادهای کریستوفل
$$
\Gamma^i_{jk} = \frac{1}{2}g^{i\ell}(\partial_j g_{k\ell} + \partial_k g_{j\ell} - \partial_\ell g_{jk})
$$

## معادله ژئودزیک
$$
\ddot x^i + \Gamma^i_{jk}\dot x^j \dot x^k = 0
$$

## تانسور ریچی
$$
\text{Ric}_{ij} = \partial_k \Gamma^k_{ij} - \partial_j \Gamma^k_{ik} + \Gamma^k_{k\ell}\Gamma^\ell_{ij} - \Gamma^k_{j\ell}\Gamma^\ell_{ik}
$$

## انحنای اسکالر
$$
R = g^{ij}\text{Ric}_{ij}
$$

## جریان ریچی
$$
\frac{\partial g_{ij}}{\partial t} = -2\text{Ric}_{ij}
$$

## کاربرد در بازار
- روند تند → انحنا زیاد → گرانش قوی
- رنج → انحنا صفر → گرانش متوسط
"""

DOCS["03_physics/HedgeMath.md"] = r"""# Hedge Mathematics

## 1. نسبت هج
$$
h_{ij} = \frac{m_j |I_i|}{m_i |I_j| + m_j |I_i|}
$$

## 2. قید هولونومیک
$$
\phi_{ij}(h) = h_{ij} - \frac{m_j |I_i|}{m_i |I_j| + m_j |I_i|} = 0
$$

## 3. ضریب لاگرانژ
$$
\lambda_i = -\frac{\langle \nabla_i \phi, F_i^\text{net}\rangle}{\|\nabla_i \phi\|^2}
$$

## 4. نیروی قید
$$
F_i^\text{hedge} = \lambda_i \nabla_i \phi
$$

## 5. تانسور قید
$$
\Phi = \begin{pmatrix} 0 & \phi_{12} & \phi_{13} \\ -\phi_{12} & 0 & \phi_{23} \\ -\phi_{13} & -\phi_{23} & 0 \end{pmatrix}
$$

## 6. تصویر روی منیفلد
$$
x^\star = x - \Phi^\top (\Phi \Phi^\top)^{-1} \phi(x)
$$

## 7. پایستگی نوتر
اگر $\mathcal{L}$ ناوردا تحت $h$:
$$
J = \sum m_i \dot x_i \cdot h_i = \text{const}
$$

## 8. کاربرد
هج = نسبت جرم خودبه‌خود. هیچ تصمیم دستی.
"""

DOCS["03_physics/OrderBookMath.md"] = r"""# OrderBookMath

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
"""

DOCS["03_physics/Physics.md"] = r"""# Physics

## Lagrangian

$$
\mathcal{L} = \frac{1}{2}\sum_i m_i \|\dot x_i\|^2 - \sum_{i<j}\frac{G_{eff}\,m_i m_j}{|x_i - x_j|} + \sum_{i<j}\lambda_{ij}\phi_{ij}
$$

where $G_{eff} = 1 / \langle d^2 \rangle_t$ is the **self-induced gravitational coupling** derived from the time-averaged squared distance between bodies (Axiom 4).

## Euler-Lagrange Equations

$$
\frac{d}{dt}\frac{\partial \mathcal{L}}{\partial \dot x_i} - \frac{\partial \mathcal{L}}{\partial x_i} = 0
$$

Yields:
$$
m_i \ddot x_i = -\sum_{j \neq i} G_{eff}\frac{m_i m_j}{|x_i - x_j|^3}(x_i - x_j) + \lambda_i \nabla_i \phi_i
$$

## Energy

$$
E = T + V
$$

$$
T = \frac{1}{2}\sum m_i v_i^2,\quad V = -\sum_{i<j}\frac{G_{eff}\,m_i m_j}{|x_i - x_j|}
$$

## Virial Theorem (Standard)

For a conservative system with only Newtonian gravity:
$$
2\langle T \rangle + \langle V \rangle = 0
$$

## Virial Theorem (Generalized)

For systems with external forces and friction (as in Concept.md §3):
$$
2\langle T \rangle + \langle V \rangle + \langle \mathbf{F}_{ext} \cdot \mathbf{x} \rangle + \langle \mathbf{F}_{friction} \cdot \mathbf{x} \rangle = 0
$$

where:
- $\mathbf{F}_{ext} = I_i \cdot m_i$ (order flow imbalance force)
- $\mathbf{F}_{friction} = -\gamma_i \cdot v_i$ (spread friction)

**Note:** This generalized form is REQUIRED for testing H2 when friction and external forces are present. The standard virial theorem ($2\langle T \rangle + \langle V \rangle = 0$) applies ONLY to the conservative subsystem (no friction, no external forces).

## Virial Theorem — Numerical Requirements (added 2026-10-07, R-PHY-001)
The identities above are statements about trajectories of the *continuous*
system with *constant* $G$. Empirically verified requirements for any test of
them (see `06_research/physics/virial_theorem.md` for full data):
1. **Dimensionality.** In 1-D every bound orbit is a radial plunge (L = 0,
   no centrifugal barrier); its close approach cannot be resolved at tick-like
   dt, so per-tick or partial-window "virial ratios" measure numerical heating,
   not physics (FailureModes F10). Circular orbits, where
   $T/V = -\frac12$ holds at every tick, exist only for configurations with
   $\|\vec L\| > 0$.
2. **Windowing.** $\langle T\rangle/\langle V\rangle = -\frac12 + O(\epsilon)$
   was measured at $\le 10^{-7}$ deviation for eccentricities up to e ≈ 0.75
   when averaging over exact integer Kepler periods; partial windows carry
   $O(10^{-2})$ bias.
3. **Precision.** float64 is required for the 1e−9-class conservation
   assertions (float32 ε ≈ 1.2e−7).
4. **Softening.** Isotropic: $d_\epsilon = \sqrt{\|\Delta x\|^2 + \epsilon^2}$
   on the full separation vector (engine fixed 2026-10-07; per-coordinate
   softening is not a central force and admits no circular orbit).

## Noether Charge

If $\mathcal{L}$ is invariant under translation, then:
$$
J = \sum m_i \dot x_i \cdot h_i = \text{const}
$$

## Angular Momentum Conservation

$$
\frac{d\vec L}{dt} = 0
$$

## Symplectic Integrator

Preserves $E$ and $\vec L$ to machine precision (for conservative subsystem).

## Self-Induced Gravity (Axiom 4)

The gravitational coupling is NOT a free parameter. It is derived from the system geometry:

$$
G_{eff}(t) = \frac{1}{\langle d^2 \rangle_t} = \frac{1}{\frac{1}{N}\sum_{i<j} |x_i(t) - x_j(t)|^2}
$$

In practice, this is computed as a running average over recent ticks to ensure stability.

> **Implementation status note (2026-10-07 audit):** the engine currently
> computes $G_{eff}$ **once from the initial state and freezes it** for the
> trajectory (`integrate()`), which is a *different* dynamical system from the
> running-average reading above (only frozen G is Hamiltonian/conservative —
> see I2). The divergence, and the degenerate-geometry fallback `G = 1.0`
> (a magic constant in disguise), are tracked as **CON-003** and analyzed in
> `06_research/physics/gravity_derivation.md` (R-PHY-002). Do not "fix" either
> side before that decision is recorded here and in Decisions.md.

**This replaces any "magic G" constant. If a constant is needed, it MUST be logged in Conflicts.md with justification.**
"""

DOCS["03_physics/Quantum.md"] = r"""# Quantum Extensions

## 1. تابع موج دفتر
$$
\psi(x, t) = A(x,t) e^{iS(x,t)/\hbar}
$$

## 2. معادله شرودینگر
$$
i\hbar \frac{\partial \psi}{\partial t} = -\frac{\hbar^2}{2m}\nabla^2\psi + V(x)\psi
$$

## 3. ترازهای انرژی
$$
E_k = \frac{\hbar^2 k^2}{2m}
$$

## 4. تفسیر
- هر سطح L2 = تراز کوانتیده
- احتمال پر بودن سطح $k$ = $|c_k|^2$

## 5. اصل عدم قطعیت
$$
\Delta x \cdot \Delta p \geq \frac{\hbar}{2}
$$

## 6. درهم‌تنیدگی سه ارز
$$
|\Psi\rangle = \alpha |BBB\rangle + \beta |BBA\rangle + \gamma |BAB\rangle + \ldots
$$

## 7. انتخاب $\hbar$
$$
\hbar = \frac{\text{tick spread}}{\text{typical volume}}
$$
"""

DOCS["03_physics/Symplectic.md"] = r"""# Symplectic Integration

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
"""

DOCS["04_market/DataSpec.md"] = r"""# DataSpec

## اسکیمای L2

### پیام Binance (`depth20@100ms`)
```json
{
  "stream": "btcusdt@depth20@100ms",
  "data": {
    "lastUpdateId": 1234567890,
    "bids": [["100.1", "1.5"], ["100.0", "3.2"], ...],
    "asks": [["100.2", "2.1"], ["100.3", "4.5"], ...]
  }
}
```

## فیلدهای نرمال‌شده
| فیلد | نوع | توضیح |
|------|-----|-------|
| symbol | str | BTCUSDT |
| bids | list[[float, float]] | ۲۰ سطح |
| asks | list[[float, float]] | ۲۰ سطح |
| ts_exchange | int ns | زمان صرافی |
| ts_local | int ns | زمان دریافت |
| seq | int | lastUpdateId |

## ذخیره‌سازی
- فرمت: Parquet
- فشرده‌سازی: zstd
- پارتیشن: symbol / day
- اندازه تخمینی: ۱ GB برای ۱۰M tick

## اعتبارسنجی
- bids strictly descending
- asks strictly ascending
- best_bid < best_ask
- همه حجم‌ها > 0
"""

DOCS["04_market/Detectors.md"] = r"""# Detectors

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
"""

DOCS["04_market/MarketMaking.md"] = r"""# Market Making

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
"""

DOCS["04_market/Microprice.md"] = r"""# Microprice

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
"""

DOCS["04_market/RegimeCatalog.md"] = r"""# Regime Catalog

## ده حالت L2

| # | حالت | امضا | پاسخ خودکار |
|---|------|-------|-------------|
| 1 | Balanced | $I \approx 0$ | گرید متقارن |
| 2 | Bid-heavy | $I > 0.3$ | هج شورت |
| 3 | Ask-heavy | $I < -0.3$ | هج لانگ |
| 4 | Thin | $m$ کوچک | گرانش ضعیف |
| 5 | Thick | $m$ بزرگ | گرانش قوی |
| 6 | Spoof | z-score > 3 | جرم کاذب حذف |
| 7 | Iceberg | refresh ≥ 3 | جرم مخفی افزوده |
| 8 | Sweep | یک سمت خالی | چرخش گیجی |
| 9 | Flash | عمق → ۰ | فریز |
| 10 | Squeeze | $I$ حاد | پادگرانش |

## جدول پارامتری

| حالت | $m$ | $I$ | $\gamma$ | $\|\vec L\|$ | اسپرد |
|------|-----|-----|----------|--------------|--------|
| Balanced | 5 | 0 | 1e-3 | متوسط | تنگ |
| Bid-heavy | 5 | +0.5 | 1e-3 | بالا | تنگ |
| Ask-heavy | 5 | -0.5 | 1e-3 | بالا | تنگ |
| Thin | 0.5 | — | 1e-3 | کوچک | گشاد |
| Thick | 20 | — | 1e-3 | بزرگ | تنگ |
| Spoof | 5 | — | 1e-3 | نامنظم | متوسط |
| Iceberg | 8 | — | 1e-3 | متوسط | تنگ |
| Sweep | 3 | ±0.8 | 5e-3 | جهش | گشاد |
| Flash | 0.1 | — | 1e-2 | صفر | فریز |
| Squeeze | 1 | +0.9 | 5e-3 | ناپایدار | گشاد |
"""

DOCS["04_market/TickModel.md"] = r"""# TickModel

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
"""

DOCS["05_implementation/Implementation.md"] = r"""# Implementation

## 1. معماری
```
L2 WebSocket → Fast Client → Detectors → Physics → MM → Grid → Simulator
```

## 2. پشته فناوری
| لایه | کتابخانه |
|------|----------|
| Loop | uvloop |
| WS | websockets |
| JSON | orjson |
| Physics | JAX |
| Detectors | numba |
| Buffer | polars |

## 3. ساختار پوشه
```
three-body-hft/
├── docs/
├── src/client/, detectors/, physics/, mm/, sim/
├── tests/
└── requirements.txt
```

## 4. جریان tick
```python
while running:
    frames = client.pop_batch(512)
    for frame in frames:
        book = parse_book(frame)
        update_detectors(frame, book)
        m_eff = correct_mass(book, detections)
        physics.set_state(i, x, m_eff, I, γ)
    physics.step()
    L = physics.angular_momentum()
    quotes = mm.quote_all(physics.state, L)
    grid = place_grid(quotes, books)
```

## 5. ضد-الگوها
❌ time.sleep در hot path
❌ pandas در hot path
❌ threading.Lock
❌ حافظه unbounded

## 6. تست
- Unit: physics, detectors, mm
- Property: L, Π, bid < ask
- Integration: ۱ ساعت زنده
"""

DOCS["05_implementation/Strategy.md"] = r"""# Strategy

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
"""

DOCS["05_implementation/roadmap.md"] = r"""# Roadmap

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
"""

DOCS["06_research/README.md"] = r"""# Research Topics — Active

Only active research lives here. Solved/closed topics move to `11_meta/`
(with a pointer left in this README). IDs are permanent: `R-<AREA>-<###>`.

## Physics Research

### [R-PHY-001] Virial Theorem for Non-Conservative Systems
- **Status:** ✅ RESOLVED (Session 2, 2026-10-07)
- **File:** `physics/virial_theorem.md`
- **Question:** Does T/V converge to −0.5? If not, what is the correct value?
- **Answer:** −0.5 holds instantaneously only for circular orbits (≥2-D) and
  as a time-average over exact integer periods for any eccentricity
  (verified to ~1e-9). The old "−1.0" was (a) a 1-D radial-plunge setup with
  numerical heating and (b) a test assignment bug. CON-002 closed.
- **Follow-ups extracted:** R-PHY-003 (resolution conditions), F10.

### [R-PHY-002] Self-Induced Gravity Derivation
- **Status:** OPEN
- **File:** `physics/gravity_derivation.md`
- **Question:** Is G_eff = 1/⟨d²⟩_t correct? Running-average vs frozen-initial
  divergence between Physics.md and `integrate()` — which satisfies Axiom 4?
- **Key constraint found:** energy conservation (I2) and the standard virial
  theorem require constant G; circular orbits are the only Kepler family
  where instantaneous and frozen G coincide.
- **Owner:** [unassigned]

### [R-PHY-003] Orbital Stability Conditions
- **Status:** PARTIAL — resolution criteria derived + measured, formal experiment pending
- **File:** `physics/orbital_conditions.md`
- **Question:** What initial conditions produce bounded ‖L‖ and numerically
  resolvable dynamics?
- **Owner:** [unassigned]

### [R-PHY-004] Generalized Virial Theorem
- **Status:** DERIVED, awaiting test implementation
- **File:** `physics/generalized_virial.md`
- **Question:** How do F_ext = I·m and friction −γ·v enter the virial?
- **Deliverable to close:** a test asserting the four-term identity with
  I≠0, γ≠0 (proposed as T-008 in `12_prompts/TaskQueue.md`).

## Detector Research

### [R-DET-001] Iceberg Detection Math
- **Status:** NOT STARTED (framing sketch in file)
- **File:** `detectors/iceberg_math.md`
- **Constraint:** detection must emerge from geometry (mass/force), no
  filters or indicators (Philosophy §2).

### [R-DET-002] Spoof Detection Math
- **Status:** NOT STARTED (framing sketch in file)
- **File:** `detectors/spoof_math.md`

## Market Making Research

### [R-MM-001] Avellaneda-Stoikov to Three-Body Mapping
- **Status:** DRAFT
- **File:** `market_making/avellaneda_stoikov_mapping.md`
- **Core tension:** A-S consumes exogenous (σ, γ, T−t); Kepler forbids
  external parameters. Mapping must be self-consistent or it is a falsification.

## General Open Problems (inherited, 10 items)
→ `open_problems.md` (was `docs/OpenProblems.md`; still Persian, translate when touched)

## How to Add a New Research Topic
1. Create a file in the appropriate subfolder of `06_research/`.
2. Add an entry here with a new `R-XXX-###` ID, status, question, owner.
3. Link from `07_hypotheses/Hypotheses.md` if the topic yields a testable claim.
4. Update `docs/00_INDEX.md` "Current Status" if it changes the headline state.
5. When resolved: keep the file (it is the record), flip status to ✅ RESOLVED,
   and reference the code/test that closes it.
"""

DOCS["06_research/detectors/iceberg_math.md"] = r"""# R-DET-001: Iceberg Detection Math

**Status:** NOT STARTED (framing only — this file defines what "started" means)
**Question:** Can iceberg replenishment be detected from orbital geometry
alone — mass `mᵢ = ln(1 + Σq)` and its derivatives — with **no filters,
no z-scores, no second-based lifetimes** (Philosophy §2.1–2.2, §2.4)?

## Why the inherited spec cannot be adopted
`04_market/Detectors.md` (still Persian, pre-protocol) defines
`score_ice = refills·(1−r_visible)·min(t/60, 1)` with thresholds
("refills ≥ 3, lifetime ≥ 5 s"). That formulation:
1. counts "refills" — requires order **identity** tracking that L2 snapshots
   do not provide (DataSpec.md: level arrays only);
2. uses wall-clock seconds — violates Axiom "time = tick" (ADR-006);
3. hard-codes 60 and 0.4 — external parameters (Philosophy §3).
It must be **re-derived**, not tuned. This is also F5's domain: a mis-modeled
iceberg is an error in the source of `mᵢ` itself, i.e. in the *gravitating
mass*, which propagates into every force — that is why detection belongs to
physics, not to indicators.

## Candidate geometric signatures (to formalize and test)
1. **Sub-Poisson depth fluctuation at fixed microprice.** Iceberg = visible
   fraction q_v constantly refreshed → level-k quantity variance at constant
   price collapses toward 0 while *trade* prints continue:
   `Var_τ(q_level k) → 0` but `μ_τ(print volume at that level) > 0`.
   Formalize via the tick-covariance `C_{qL}(Δt) = Cov(q_k(t), q_k(t+Δt))` —
   normal books decay, iceberg books show a floor.
2. **Mass inertia mismatch.** In `m = ln(1+Σq)`, an iceberg adds large true
   volume with small apparent volume → the body responds to `I` (drive)
   *too sluggishly* relative to its printed flow: mismatch
   `‖Δẍ_grav‖ expected from prints − measured ‖Δẍ‖`. Detection = model
   residual of the EOM, not a threshold on a score.
3. **Force-conservation residual.** Since all accelerations come from
   pairwise G mᵢmⱼ, hidden mass violates the internal consistency between
   relative acceleration of the three bodies and their *visible* masses;
   residual → effective-mass correction term (analogous to dark matter
   inference). A principled estimator: infer `m̂` from orbital dynamics
   (least-squares on one tick-window of the integrated EOM) and compare
   with book-derived `m`. `m̂ ≫ m` ⇔ hidden depth. This is the only
   filter-free definition consistent with the axioms.

## Required before R-DET-001 is "started"
- Write the estimators on synthetic two-state book generators (ice vs.
  natural replenishment), all quantities in ticks.
- Falsifiable criterion tied to `07_hypotheses/Falsifiability.md`; expected
  failure mode = F5 with quantified mass error.
- Only then touch `src/` (roadmap Phase 3 / T-005 depends on this file).

## Owner / next action
[unassigned] — Start by formalizing estimator (3); it doubles as a test of
Axiom 3 (mass ≡ depth) and would be falsified by any m̂–m correlation drift.
"""

DOCS["06_research/detectors/spoof_math.md"] = r"""# R-DET-002: Spoof Detection Math

**Status:** NOT STARTED (framing only)
**Question:** Can spoofing (large far-from-mid orders placed to induce a
false potential gradient, cancelled before trade) be detected as a *dynamical*
property of the mass field rather than a cancel-rate statistic?

## Inherited spec's problems (same audit as R-DET-001)
`Detectors.md` spoof score uses z-score, cancel/fill ratio, bps distance,
seconds-based age, and an exponential `e^{−d/100}` — indicators + wall-clock
+ magic constants. Not admissible; must be re-derived geometrically.

## Geometric view of a spoof
A spoof is a **pulsed, non-Keplerian mass perturbation**: it enters `m` and
`Σq` instantly, perturbs every other body's acceleration through
`G m_i m_j/d³`, and vanishes without exchanging momentum via trades.
Legitimate depth changes propagate through microprice motion `ẋ` and
imbalance `I`; a pure cancellation changes `m` with **no matching impulse
in the momentum ledger** (no trades, no queue-position decay of the level).

Candidate signatures (formalize in tick units, no thresholds from outside):
1. **Mass-jump / action-conservation residual.** Between ticks, compare
   `Δm_i` against the impulse implied by trade prints at that body's book.
   Spoof: `|Δm| ≫ impulse mass moved`. Quantify as the violation of the
   EOM's mass-source consistency across a whole 3-body window — one scalar,
   shared with R-DET-001 estimator (3).
2. **Curvature anomaly in the γ channel.** Spread/friction `γ = spread/x`
   spikes when far levels appear (they widen effective distance statistics?)
   — weak; keep as secondary.
3. **Larmor-like radiation analogy:** accelerating a test body by moving a
   source mass in and out with no transport is like driving the field
   without injecting momentum; measure `Σᵢ ∮ Fᵢ·dxᵢ` over a tick window —
   a conservative book change leaves the closed-loop work ≈ 0; pulsed
   spoofing injects net loop work. Connects to H3 (Π = ∮p·dx).

## Required before "started"
Same gate as R-DET-001: synthetic spoof generator + geometry-only estimators
+ a rejection criterion written into `07_hypotheses/` first. Falsification
mode to watch: a legitimate market-maker requote pattern triggers it
(that would be a genuine model failure — log under F5/F9).

## Owner / next action
[unassigned] — jointly scope estimators (1)+(3) with R-DET-001 (they share
the mass-source-consistency primitive; build once).
"""

DOCS["06_research/market_making/avellaneda_stoikov_mapping.md"] = r"""# R-MM-001: Avellaneda–Stoikov → Three-Body Mapping

**Status:** DRAFT (audit of the inherited mapping; several terms are not
yet self-consistent)
**Question:** Which A-S object, if any, is *identical* (not merely analogous)
to a Kepler geometric quantity, under the no-external-parameters rule?

## Inherited mapping (04_market/MarketMaking.md, Persian legacy table)
| A-S quantity | Claimed Kepler counterpart | Audit verdict |
|---|---|---|
| risk aversion γ_AS | `1/‖L‖` | **Dimensionally arbitrary**: ‖L‖→0 ⇒ spread→∞ is a *story*; needs derivation from an optimization with tick-time, not substitution |
| inventory q | `m·v` (momentum) | Plausible *direction* (signed momentum ~ signed inventory) but q accumulates *trades*; `m·v` is model state — equivalence must be derived via the trade-driven update law of `v`, else rejected |
| mid s | `x_i` (log microprice) | ✅ definition-level match by construction (Concept §2.2) |
| σ² | `‖F_grav‖/m` | **Diverges from A-S semantics**: σ² is the *diffusion of s*, not acceleration; propose σ̂² from realized tick increments of x — but that is an estimator/filter → conflicts with Philosophy §2 unless it is the field itself |
| fill intensity k | "constant" | ❌ an explicit magic constant — violates Axioms; must become `I`-driven arrival rate or be falsified |
| horizon T−t | ticks remaining | A-S terminal horizon presumes *calendar* time; time=tick ⇒ T−t is only meaningful as a tick count → keep, but re-derive HJB in discrete time |

## Structural tension (why this stays "DRAFT")
A-S solves a stochastic-control problem whose controls (quotes) feed back on
s through fills; Kepler's quotes are *the same bodies' positions* — the map
mixes an optimizer with a simulator. Either:
(a) the Kepler orbit reproduces the A-S optimal *policy* for some parameter
regime (then A-S is a corollary — strong, falsifiable claim: compare quoted
δ± against r ± (½)Gm²/d² for one synthetic regime), or
(b) the mapping is heuristic and must be demoted to "Motivating Analogy" in
`11_meta/References.md`.
Recommendation: attempt (a) on the circular-orbit regime (the only exactly
solvable one, see R-PHY-001) before touching any market-maker code (T-006).

## First concrete experiment (for whoever picks this up)
Closed-form check on the circular orbit: reservation shift
`r = x − q γ_AS σ²(T−t)` with (q,m,v) and G_eff substituted — compute whether
the A-S bid/ask ladder, when re-inserted as *books*, keeps the orbit circular
(self-consistency loop). If the loop diverges for all parameters, H8-style
claim dies immediately — that is a cheap, decisive falsification.

## Owner
[unassigned]
"""

DOCS["06_research/open_problems.md"] = r"""# Open Problems

> Editor's note (2026-10-07, Session 2): legacy list, still Persian; kept
> verbatim. Tracked status now lives per-topic in this folder
> (`physics/`, `detectors/`, `market_making/`, registry in `README.md`).
> #1 (gravity↔repulsion) and #7 (quantized time) intersect CON-003/R-PHY-002.

## 1. جاذبه vs دافعه
در همبستگی منفی، گرانش نیوتنی اشتباه است. مدل جدید لازم است.

## 2. علامت $\gamma$
آیا $\gamma$ باید منفی شود در رژیم‌های خاص؟

## 3. درهم‌تنیدگی سه ارز
آیا ارزها واقعاً درهم‌تنیده‌اند یا جدا؟

## 4. نقش اطلاعات
آیا آنتروپی می‌تواند به‌عنوان پتانسیل اضافی عمل کند؟

## 5. حد $\hbar$
آیا ثابت پلانک بازار قابل اندازه‌گیری است؟

## 6. چند صرافی
آیا سه ارز در سه صرافی = ۹ جسم؟

## 7. زمان کوانتیده
آیا tick یک کوانتوم واقعی است یا فقط گسسته‌سازی؟

## 8. قضیه نوتر معکوس
آیا هر ناوردا یک تقارن دارد؟

## 9. آستانه Chaos
آیا بازار در رژیم chaos است؟

## 10. نظریه واحد
آیا فیزیک + اطلاعات + هندسه یک کل را می‌سازند؟
"""

DOCS["06_research/physics/generalized_virial.md"] = r"""# R-PHY-004: Generalized Virial Theorem (driven + damped Kepler)

**Status:** DERIVED (this document), test pending → T-008 in TaskQueue.
**Question:** How do the imbalance drive `F_ext,i = I_i·m_i` and the spread
friction `F_fric,i = −γ_i·v_i` enter the virial identity, and what should H2
claim in their presence?

## Derivation
Define the scalar virial `G_v = Σᵢ pᵢ·xᵢ` (note: distinct from self-induced
`G`; symbol clash acknowledged — docs use `G_v`). For masses fixed per epoch
(Axiom 3 — m only changes when L2 changes):

```
dG_v/dt = Σᵢ ṗᵢ·xᵢ + Σᵢ pᵢ·vᵢ = Σᵢ Fᵢ·xᵢ + 2T
```
For bounded motion G_v stays bounded, so its mean rate vanishes:
`(G_v(τ) − G_v(0))/τ → 0` as τ → ∞. Time-averaging over τ:

```
2⟨T⟩ + ⟨Σᵢ Fᵢ·xᵢ⟩ = 0
```

Split `Fᵢ = Σ_{j≠i} f_ij + mᵢIᵢ − γᵢvᵢ`. Central pairwise forces give the
usual `⟨Σᵢ Σ_j f_ij·xᵢ⟩ = ⟨V⟩` (V ∝ 1/d homogeneous, softened corrections
enter as ⟨O(ε²/d²)⟩ — negligible once orbits are collision-resolved per
R-PHY-003). Hence the **generalized virial identity of the Kepler game**:

```
        2⟨T⟩ + ⟨V⟩ + ⟨Σᵢ mᵢ Iᵢ·xᵢ⟩ − ⟨Σᵢ γᵢ |vᵢ|²⟩ = 0
```

or in ratio form, the corrected equilibrium condition:

```
⟨T⟩/⟨V⟩ = −½ · [ 1 + ( ⟨Σ mᵢIᵢxᵢ⟩ − ⟨Σ γᵢ|vᵢ|²⟩ ) / ⟨V⟩ ]
```

## Consequences for H2 and the market interpretation
1. **−0.5 is a special-case prediction** (I = 0, γ = 0). The market state is
   never that: `I` and `γ` are first-class observables (Concept §2.4–2.5). So
   H2 cannot claim "T/V → −½" for live L2; it claims the **four-term identity
   above**. Deviation of the instantaneous T/V from −½ is *signal*, not noise:
   it measures the signed work of imbalance minus dissipation.
2. Friction alone (I = 0) drives ⟨T⟩ down: a damped pair falls toward the
   softening core → exactly the F10 regime unless I pumps it. In tick terms:
   pure-spread-friction books collapse orbits; sustained imbalance is required
   to keep "market" orbits resolved. This interaction (γ vs I vs core plunge)
   deserves its own experiment.
3. For the circular test orbit: v·x = 0 (friction term vanishes instant by
   instant) and ⟨xᵢ⟩ = 0 (COM-centered) so a *constant* I contributes nothing
   on average — the correction terms are genuinely second-order for that
   family, which is why R-PHY-001's conservative test remains a valid special
   case. Non-constant (tick-varying) I, γ is the live regime.
4. Physics.md already states this generalized form correctly — this document
   supplies the derivation it referenced, closing the loop for CON-002's
   "implement generalized virial theorem" resolution step.

## Proposed test (T-008, to be written by the next session)
Config: 2-D pair, moderate ellipse (k ≈ 0.9), I = const ≠ 0 (small enough that
orbits stay collision-resolved per R-PHY-003 preflight), γ = 0.1·spread-like.
Assert the four-term identity |2⟨T⟩ + ⟨V⟩ + ⟨Σ mIx⟩ − ⟨Σγ|v|²⟩| / |⟨V⟩| < 0.2
(0.2 inherited from I4 — do not invent a new threshold; if the identity fails
beyond it, that is a falsification of THIS document → FailureModes F9).
Window: integer Kepler periods at current G (R-PHY-003 window rule).

## Status
DERIVED / awaiting empirical closure (T-008). If T-008 fails with clean
preflight, mark F9 violated and re-examine the softening correction term.
"""

DOCS["06_research/physics/gravity_derivation.md"] = r"""# R-PHY-002: Self-Induced Gravity Derivation

**Status:** OPEN (Session 2 findings recorded; decision required — human/ADR)
**Question:** Is `G_eff = 1/⟨d²⟩_t` the right realization of Axiom 4, and in
which sense does the code implement it?

## What the code actually does (audited 2026-10-07)
`compute_self_induced_G()` computes `G = 1 / mean_pairwise(‖dx‖²)` from the
**initial** state, and `integrate()` **freezes it for the whole trajectory**.
`03_physics/Physics.md` claims a *running average over recent ticks*.
These are different dynamical systems:

| Property | frozen G (impl) | running G (Physics.md text) |
|---|---|---|
| Hamiltonian / symplectic | ✅ yes | ❌ no (explicitly time-dependent coupling) |
| I2 "E = const to machine precision" | ✅ testable | ❌ violated by construction |
| Axiom 4 "self-consistent adaptation" | only at t=0 | literal reading |

**This spec↔impl divergence is not yet a bug — it is the open decision.**
Either the theorem set (I2, standard virial) must be restricted to the frozen-
G subsystem, or a time-dependent-G invariant (generalized, R-PHY-004) must
replace them. Proposed as ADR-008 candidate; also candidate conflict CON-003
below.

## Properties of G_eff = 1/⟨d²⟩ (why it is defensible)
Let positions live in ln-microprice space, so `d` is dimensionless and
`G = 1/⟨d²⟩` is a pure number — no units, no free constant, positive definite,
and **scale-seeking**: pairs closer than unit log-distance interact strongly,
farther pairs interact weakly (force ∝ G·m/d² = m/d⁴ at the pair level for a
single pair — one power steeper than Newton). Consequences to examine:

1. **Effective exponent.** Substituting G_eff into the pair potential gives
   V_pair ∝ −1/(⟨d²⟩·d). For a single pair with ⟨d²⟩ = d² this is
   V ∝ −1/d³ — a *steeper-than-Kepler* potential. The standard virial ratio
   for homogeneous V ∝ rⁿ is ⟨T⟩/⟨V⟩ = n/2, i.e. **−3/2 for n = −3, not −1/2.**
   → Any H2-style claim must pin down whether ⟨d²⟩ is the *same* d that enters
   the force law. The current test (R-PHY-001) dodges this entirely because a
   circular orbit keeps d ≡ d₀, so frozen G = instantaneous G and the orbit is
   a genuine Kepler (n = −1) orbit under that constant G. Non-circular
   configurations do NOT dodge it.
2. **Degenerate guards.** `compute_self_induced_G` returns the magic value
   `1.0` when mean d² < ε (single-body or co-located books) — this is a
   G_DEFAULT in disguise and contradicts the CON-001 resolution. Should it
   instead return `1/ε` (the continuous limit) or 0 (decoupled)? NEEDS DECISION.
   Also `compute_virial_ratio` guards |V| < ε by substituting ε, which produced
   the giant spurious per-tick ratios documented in R-PHY-001 — the guard hides
   escape instead of reporting it.
3. **Noether charges.** A frozen G preserves translation symmetry → total
   momentum; running G is still translation-invariant but explicitly time-
   dependent → energy non-conservation is the expected channel, see R-PHY-004.

## Alternatives on the table (untested)
- `G = 1/⟨d²⟩_t` running average over a window W (W = ? ticks — window length
  would itself be an external parameter unless W = t, a causal cumulative mean).
- `G = c/⟨d⟩²` etc. — rejected without experiment (adds no symmetry).
- Keep frozen-initial G (current code) and *document Axiom 4 as an initial-
  condition calibration*: G is set by the first tick's geometry, then the game
  is conservative until the next "epoch". Simplest to reconcile with I2/I4.

## Proposed verification experiments (next sessions)
- E1: measure ⟨T⟩/⟨V⟩ for a 2-D *elliptical* orbit under (a) frozen G and
  (b) true running G. Prediction: (a) → −0.5 (R-PHY-001 table already shows
  it — because with d ≢ d₀ the *frozen* G is constant while ⟨d²⟩ varies; the
  deviation measured there was ~1e-8, so running-vs-frozen must be the
  discriminator, not eccentricity alone), (b) → systematic drift.
- E2: unit test pinning the degenerate-case G so the magic 1.0 is either
  justified in Conflicts.md or removed.

## Decision needed
Record outcome in `11_meta/Decisions.md` (new ADR) and update `Physics.md`,
`Axioms.md` untouched (human-only file).

## Status
OPEN — assigned next-session priority: HIGH (blocks the honest wording of H2
beyond circular orbits, and of I2 beyond the frozen-G subsystem).
"""

DOCS["06_research/physics/orbital_conditions.md"] = r"""# R-PHY-003: Orbital Stability & Resolution Conditions

**Status:** PARTIAL (criteria derived and spot-verified 2026-10-07; formal
experiment pending — proposed T-009)
**Question:** Which initial configurations produce bounded ‖L‖, bounded
motion, and a numerically resolvable trajectory under the frozen-G engine?

## Two separate notions of "stability" (auditing found these conflated)
1. **Physical boundedness** (continuous system, frozen G):
   `E = T + V < 0` ⇔ bound (V → 0 at infinity). For the pair benchmark
   (m = 1, d₀ = 2, G = ¼, tangential v at d₀):
   `E = μ v_rel²/2 − G m²/d₀`, μ = ½ ⇒ bound ⇔ v_rel < √(2G m²/d₀ · (2/1))…
   numerically: per-body speed v < v_circ·√2 = 0.3536 (escape at k ≥ √2).
2. **Numerical resolvability** (discrete leapfrog, dt = 1 tick-step):
   close approaches must satisfy `dt · ω(r_min) ≪ 1`, and
   `r_min ≫ ε = 1e−8`. In **1-D every bound orbit is radial (L = 0)** with
   r_min → ε: *no* conservative 1-D bound test can be resolved at tick-like
   dt (verified: dt = 1e−3 heats E from −0.115 to +296; dt would need to be
   ~1e−12). This is the F10 mechanism and it is a **theorem of the 1-D setup**,
   not a tuning accident — do not "fix" it with smaller thresholds; fix it
   with a centrifugal barrier (≥ 2-D) or non-conservative driving.

## Angular momentum
For the central gravitational force law (isotropic softening, fixed G),
‖L‖ is exactly conserved by the pair force (internal forces are central);
measured |ΔL| ≤ 1e−14 over 2e5 ticks, float64. Channels that change L:
- `I_i` drive: constant imbalance exerts a uniform force → torque
  τ = Σ mᵢxᵢ × I (zero for COM-centered symmetric pairs, linear drift
  O(‖x‖·I·t) otherwise);
- friction `γ_i v_i`: damps the *orbital* motion → L bounded and decaying.
So H1 (‖L‖ bounded) is *guaranteed in the conservative sector* and is only
informational in the driven sector — recorded so future agents stop
re-deriving it.

## Measured map (pair benchmark, float64, dt = 1e−4, n = 2e5,
## post-skip time average of T/V over ~1 period)

| k = v/v_circ | state | E drift (rel) | ⟨T⟩/⟨V⟩ dev | verdict |
|---|---|---|---|---|
| 1.00 | exact circle | 4.9e−14 | 1.2e−10 | ✅ canonical H2 test config |
| 0.95 | mild ellipse | 8.6e−11 | 1.6e−2 → 5e−10 @1 period | ✅ if window = integer periods |
| 0.80 | e = 0.36 ellipse | 1.3e−9 | 1.1e−3 → 6.5e−8 @1 period | ✅ same caveat |
| 0.60 | e = 0.64 ellipse | 3.1e−8 | 6.6e−2 → 1.4e−7 @1 period | ⚠️ window bias ≫ for short windows |
| 0.50 | e = 0.75 ellipse | 1.8e−7 | 4.9e−2 → 7.4e−8 @1 period | ⚠️ needs dt ↓ near r_min |
| ≥ 1.4142 | E ≥ 0 | grows | guard-divide artifacts | ❌ escape; invalid for H2 |
| 1-D any | radial plunge | 1e+03 scale jump | meaningless | ❌ F10 |

(The "@1 period" column uses exact Kepler-period windows, dt = 2e−5 —
see `virial_theorem.md` verification table. Partial windows carry
O(remaining-phase/total-window) bias, which is *expected* for the ratio of
averages and is the reason I4 must state its window rule.)

## Recommended invariant for a "healthy-orbit" preflight (to add to QA later)
A conservative test trajectory is admissible iff, over the whole run:
`min separation ≥ C · dt · max|v|` (collision-resolved), `E` relative drift
< 1e−9, and `max|v| ≤` continuous-orbit bound √(2|V(r_min)|) within 1%.
Fail any of the three → the *setup* is invalid (log F10-class note), do not
touch thresholds.

## Next (T-009)
- Encode the admissibility preflight as a helper in `tests/` and apply it to
  every future conservative-invariant test.
- Sweep eccentricity × dt to produce the formal stability boundary plot/table
  for `10⁻⁵ ≤ dt ≤ 10⁻³`.

## Status
PARTIAL — no open contradictions; deliverable is the preflight helper + sweep.
"""

DOCS["06_research/physics/virial_theorem.md"] = r"""# R-PHY-001: Virial Theorem for Non-Conservative Systems

**Status:** ✅ RESOLVED (2026-10-07, Session 2) — see "Resolution" below.
**Related:** CON-002 (closed), F8, F10 (new), I4, H2 (revised), R-PHY-003/004.

## Question
Does `T/V` converge to −0.5 for the Kepler three-body system, and what does
a persistent −1.0 mean?

## Background
For a homogeneous potential V ∝ rⁿ (n = −1 for Newton), the time-averaged
virial theorem states

```
2⟨T⟩ + ⟨V⟩ = 0        ⇔        ⟨T⟩/⟨V⟩ = −1/2
```

for any bounded trajectory of the **conservative** system, where ⟨·⟩ is a
long-time average. Prerequisites that are easy to violate in tests:

1. **Bounded motion with bounded virial** G = Σ pᵢ·xᵢ — ⟨Ġ⟩/2τ → 0 fails if
   the system escapes.
2. **Conservativeness** — imbalance drive `Iᵢ` and friction `γᵢ` add terms
   (→ R-PHY-004).
3. **A faithful trajectory** — the average is of the *continuous* orbit; if
   the discrete integrator is unresolved, ⟨T⟩ and ⟨V⟩ are averages of a
   different (non-Keplerian) system.

## The Reported Failure (pre-fix)
`test_virial_ratio_convergence` reported `⟨T⟩ = 376741, ⟨V⟩ = −376446,
ratio = −1.0008` with 1-D initial conditions x = ∓1, v = ±0.1,
m = 1, dt = 1e−3, n = 20 000. Two *compounding* defects were found:

### Defect A — the test measured nothing (assignment bug)
`integrate()` returns `(L_norm, energy, virial, imbalance_abs)` — the third
array is the **per-tick ratio** T/V, not the potential. The old test bound it
to a variable named `V` and computed `T = E − V`, so:

- "⟨V⟩" = −376 446 was actually ⟨T/V⟩ — dominated by `compute_virial_ratio`'s
  division guard (`V := ε` when |V| < ε) after the escaping pair drove the
  true potential to ~0, giving |T/V| ~ T/1e−8 ~ 1e9–1e10.
- "⟨T⟩" = ⟨E − T/V⟩ was fabricated.
- Hence "ratio" = (Ē − V̄)/V̄ = **Ē/V̄ − 1 ≈ −1.00079**. The famous −1.0 was an
  algebraic echo of −1 plus a tiny energy/pseudo-potential quotient — not a
  physical measurement, not a model falsification.

### Defect B — the setup was unphysical (1-D has no circular orbits)
In one spatial dimension every bound two-body orbit has zero angular momentum:
it is a **radial plunge** through the ε-softened core (F10 mechanism). Measured
(x64, dt = 1e−3): close approaches are unresolved — |v| ≈ 17 at
separation ≈ 4.5e−3, leapfrog scatters the pair, total energy heats from
−0.115 to **+296** and the system escapes. The inherited handoff's
recommended fix — "use v_circ = √(G(m₁+m₂)/r₀)" — **does not work in 1-D**:
with v = v_circ the same plunge occurs (E: −0.0625 → +160), because
v_circ only defines the *apoapsis speed* of a radial orbit, not an orbit of
constant radius. A circular orbit requires a centrifugal barrier, i.e. **≥ 2-D
configuration space**. (This is why the engine also needed the multi-D fix —
see "Engine change".)

Note: the deeper the plunge, the worse the resolution; the pair reaches
sep ~ ε = 1e−8 only if steps resolve |v| ~ 7e3 (dt ≲ 1e−12). No threshold
change can rescue such a configuration — and per QA_Protocol P3 none was made.

## Resolution

### 1. Correct conservative test configuration: 2-D circular orbit
Two equal masses m = 1 at x = (∓1, 0); self-induced coupling from the initial
state: G = 1/⟨d²⟩ = 1/4 (Axiom 4, exactly as `integrate()` freezes it).
Per-body centripetal balance at radius r = d/2 = 1:

```
m v² / r = G m² / d²   ⇒   v_circ = √(G·m·r)/d = √(0.25·1·1)/2 = 0.25
(equivalently v_rel = √(G(m₁+m₂)/d) = 0.5 split equally between bodies)

T = ½·2·m·v_circ² = G m²/(2d)  = +0.0625      V = −G m²/d = −0.125
⇒  T/V = −1/2   EXACTLY, constant at every tick (r ≡ d for a circle).
```

The circular orbit is also the unique Kepler family for which
⟨d²⟩ = const, so "frozen initial" G ≡ "running-average" G — the test is
simultaneously a test of Axiom 4's self-consistency (see R-PHY-002).

### 2. Engine change (enabler)
`compute_potential_energy`, `acceleration`, `compute_self_induced_G` used
**per-coordinate** softening `√(dx_k² + ε²)`, so any multi-D configuration was
an anisotropic non-central force (and `compute_potential_energy` returned a
vector for 2-D states). Fixed to **isotropic** softening
`dist = √(‖dx‖² + ε²)`; `acceleration` returns `zeros_like(x)` shapes.
1-D outputs are bit-identical (jnp.sum of a scalar); 9/9 tests confirm.

### 3. Verification (measured 2026-10-07, jax float64, dt = 1e−3, n = 20 000)
Test `test_virial_ratio_convergence` (rebuilt):
- mean |⟨T/V⟩ + 0.5| = **1.2e−10** ; per-tick max |T/V + 0.5| ≪ 0.2 (asserted)
- energy relative drift = 4.9e−14 (I2 side-check on the same trajectory)
- ‖L‖ = 0.500000 constant (H1, |ΔL| ≤ 1.2e−14)

Stronger cross-check — the theorem holds for ANY eccentricity when averaged
over exact integer periods (dt = 2e−5; deviation from −0.5 of ⟨T⟩/⟨V⟩):

| v/v_circ | a | r_min | r_max | periods | deviation |
|---------|------|-------|-------|---------|-----------|
| 1.00 | 1.000 | 2.000 | 2.000 | — | 1.2e−10 (exact instantaneously) |
| 0.95 | 1.822 | 1.645 | 2.000 | 1 | 5.4e−10 |
| 0.90 | 1.681 | 1.361 | 2.000 | 1 | 2.9e−8 |
| 0.80 | 1.471 | 0.941 | 2.000 | 1 | 6.5e−8 |
| 0.80 | 1.471 | 0.941 | 2.000 | 10 | 1.8e−9 |
| 0.60 | 1.220 | 0.439 | 2.000 | 1 | 1.4e−7 |

Partial-window averaging (e.g. the old test's 20·1e−3 = 0.8–1.5 periods)
leaves a bias of a few ×10⁻² — still ≪ 0.2, but the honest statement is:
**time-average over integer periods, or circular orbits, not per-tick.**

## Conclusions
1. H2 as "per-tick T/V → −1/2 for any bound orbit" is **false** — per-tick
   T/V ranges over (−1, 0) on ellipses (measured: e.g. v ∈ [−0.875, −0.125]
   at k = 0.5). −0.5 per tick ⇔ circular orbit (plus instantaneous-ε terms).
2. H2 as "⟨T⟩/⟨V⟩ → −1/2 over long averages, conservative subsystem" is
   **true and now passing** — the theorem survived; the test died first.
3. A "−1.0 virial ratio" in this engine is a **signature of unresolved
   close-approach/escape dynamics or the guard-divide artifact** — logged as
   F10 so no future agent re-misreads it as a model falsification.

## Status
RESOLVED — fix in `tests/test_physics.py::test_virial_ratio_convergence` +
engine isotropic softening + `tests/conftest.py` float64.
Hypotheses.md H2 revised accordingly. Follow-ups → R-PHY-003, R-PHY-004, T-008.
"""

DOCS["07_hypotheses/Experiments.md"] = r"""# Experiments

## E1 — شبیه‌سازی ۱۰ میلیون tick
**هدف:** تست H1, H2, H3.
**داده:** Binance BTC/ETH/SOL.
**معیار:** $\Pi > 0$ با CI 95%.

## E2 — ده حالت L2
**هدف:** تست H6.
**داده:** داده ساختگی کنترل‌شده.
**معیار:** پاسخ صحیح در ≥8 حالت.

## E3 — آزمون شکست
**هدف:** تست H5.
**داده:** گپ‌های تاریخی.
**معیار:** بازگشت در <10 tick.

## E4 — آزمون پایستگی
**هدف:** تست H7.
**داده:** ۱۰۰٬۰۰۰ tick.
**معیار:** $\|\phi\| < 10^{-6}$.

## E5 — مقایسه با A-S کلاسیک
**هدف:** برتری نگاشت هندسی.
**داده:** همان داده.
**معیار:** Sharpe بالاتر.

## E6 — آزمون Cross-timeframe
**هدف:** سازگاری در 1m, 5m, 1h.
**معیار:** همبستگی مدار > 0.7.

## E7 — آزمون چندجهانی
**هدف:** سه تایم‌فریم موازی.
**معیار:** همگام‌سازی بدون واگرایی.

## طرح آماری
- t-test زوجی
- Bootstrap ۱۰٬۰۰۰ نمونه
- تصحیح بنفرونی $\alpha/n$
"""

DOCS["07_hypotheses/Falsifiability.md"] = r"""# Falsifiability

## اصل
هر ادعا باید قابل رد باشد.

## ادعاهای اصلی و شرایط رد

### A1 — مدار پایدار
**رد:** $\|\vec L\| \to \infty$ در زمانی متناهی.

### A2 — هج حفظ می‌شود
**رد:** انحراف $\phi$ از صفر.

### A3 — سود مثبت
**رد:** $\mathbb{E}[\Pi] < 0$ با CI 95%.

### A4 — فریز خودکار
**رد:** حجم کوتیشن غیرصفر وقتی $\|\vec L\| = 0$.

### A5 — تطبیق در ۱۰ حالت
**رد:** شکست سیستماتیک در ≥۳ حالت.

### A6 — همبستگی با انحنا
**رد:** همبستگی $\Pi$ و $\int\|\vec L\|$ < 0.3.

## سه حالت شکست پیش‌بینی‌شده
1. Jump-to-zero depth
2. Cross-exchange divergence
3. Exogenous shock

این‌ها **پیش‌بینی‌های ردکننده** هستند.

## چه چیزی این سیستم را کاملاً رد می‌کند؟
- اگر $\vec L$ پایسته نباشد.
- اگر سود در ۱۰۰٬۰۰۰ tick منفی باشد.
- اگر فریز خودکار کار نکند.
"""

DOCS["07_hypotheses/Hypotheses.md"] = r"""# Hypotheses

## H1 — Orbital Stability
**Claim:** $\|\vec L\|$ is bounded.
**Rejection criterion:** $\|\vec L\| > 10 \bar{L}$ in >5% of time.

## H2 — Virial Equilibrium (REVISED 2026-10-07, post R-PHY-001)
**Original claim:** $T/V \to -1/2$ (per tick, any bound orbit).
**Revised claim:** $\langle T\rangle/\langle V\rangle \to -1/2$ over time
averages spanning exact integer orbital periods for the **conservative
subsystem** ($I=0,\ \gamma=0$, frozen $G$); for circular orbits it holds
instantaneously at every tick. In the general case the testable statement is
the generalized identity $2\langle T\rangle + \langle V\rangle +
\langle\sum_i m_i I_i x_i\rangle - \langle\sum_i \gamma_i |v_i|^2\rangle = 0$
(`06_research/physics/generalized_virial.md`).
**Rejection criterion:** Deviation > 20% (0.2 absolute on the ratio) in 90% of
time — magnitude UNCHANGED from Invariants.md I4; only the averaged quantity
and the period/window rule are now specified.
**Status:** Passing in the circular-orbit regime (`test_virial_ratio_convergence`,
deviation ~1e-10). Generalization pending R-PHY-004/T-008.
**Evidence:** `06_research/physics/virial_theorem.md`, `FailureModes.md` F10.

## H3 — Profit = Curvature
**Claim:** $\Pi \propto \int \|\vec L\| dt$.
**Rejection criterion:** Correlation < 0.5.

## H4 — Freeze on Linear
**Claim:** $\|\vec L\| = 0 \Rightarrow Q = 0$.
**Rejection criterion:** Quoted volume in this state > 0.

## H5 — Recovery After Gap
**Claim:** After a gap, orbit returns to initial state.
**Rejection criterion:** No recovery within <10 ticks.

## H6 — Filter-Free Adaptation
**Claim:** System behaves correctly in all 10 L2 states.
**Rejection criterion:** Failure in ≥2 states.

## H7 — Hedge Invariance
**Claim:** $\phi(h) = 0$ always.
**Rejection criterion:** Deviation > 1e-6.
"""

DOCS["07_hypotheses/Invariants.md"] = r"""# Invariants

## Fundamental Invariants

### I1 — Angular Momentum
$$
\frac{d\vec L}{dt} = 0 \quad \text{(no external torque)}
$$

### I2 — Total Energy
$$
E = T + V = \text{const} \quad \text{(closed system)}
$$
> Scope note (2026-10-07): "const" is meaningful only for the conservative
> subsystem with **frozen G** (see R-PHY-002: running G would break it by
> construction). Verification additionally requires float64 — the 1e−9 bound
> lies below float32 machine epsilon (see `tests/conftest.py`).

### I3 — Hedge Constraint
$$
\phi(h) = 0
$$

### I4 — Virial Ratio
$$
2\langle T \rangle + \langle V \rangle = 0
$$
> Clarified 2026-10-07 (R-PHY-001 / H2 revision): the averages are
> time-averages over exact integer orbital periods of the conservative
> subsystem ($I=0,\gamma=0$, frozen $G$); per-tick $T/V\equiv-\tfrac12$ holds
> only for circular orbits. The threshold |⟨T⟩/⟨V⟩ + 0.5| < 0.2 is FIXED
> (QA P3) and requires float64 + a collision-resolved trajectory
> (`FailureModes.md` F10, preflight in `06_research/physics/orbital_conditions.md`).

### I5 — Total Mass
$$
\sum_i m_i = \text{const} \quad \text{(no volume exchange)}
$$

### I6 — Normalized Imbalance
$$
|I_i| \leq 1
$$

### I7 — Bid < Ask Constraint
$$
\text{Bid}_i < \text{Ask}_i
$$

## Tests
| Invariant | Test | Criterion |
|-----------|------|-----------|
| I1 | `test_physics.py` | Relative error < 1e-9 |
| I2 | `test_physics.py` | Same |
| I3 | `test_mm.py` | |φ| < 1e-6 |
| I4 | `test_physics.py` | |V + 0.5| < 0.2 |
| I5 | `test_sim.py` | drift < 1% |
| I6 | `test_detectors.py` | Always |
| I7 | `test_mm.py` | Always |
"""

DOCS["08_failures/Conflicts.md"] = r"""# Conflicts

## Status: Active conflicts require resolution.

## CON-001: ADR-007 G_DEFAULT violates Axiom 4
**Date:** 2026-10-07
**Files:** `11_meta/Decisions.md` (ADR-007) vs `01_foundation/Axioms.md` (Axiom 4)
**Description:** ADR-007 introduced G_DEFAULT = 1e-6 as a magic constant for
log-price positions. This violates Axiom 4 which requires self-induced gravity
without free parameters.
**Severity:** HIGH
**Resolution proposed:** Reject ADR-007. Implement G_eff = 1 / <d²>_t
(time-averaged squared distance). Update Physics.md with self-induced gravity
formula.
**Status:** RESOLVED — ADR-007 rejected, Physics.md updated.

## CON-002: Virial test threshold vs Invariants.md I4
**Date:** 2026-10-07
**Files:** `tests/test_physics.py` vs `07_hypotheses/Invariants.md` (I4)
**Description:** The virial test threshold had been loosened to 1e-5 in an
earlier attempt to make tests pass. Invariants.md specifies
|⟨T⟩/⟨V⟩ + 0.5| < 0.2 for I4, and the generalized virial theorem must be
implemented for driven/damped systems. Test measured "T/V → −1.0".
**Severity:** MEDIUM
**Resolution proposed:** Implement generalized virial theorem (see Physics.md).
If test still fails, log as falsification in FailureModes.md. Do NOT loosen
threshold.
**Status:** RESOLVED — 2026-10-07 (Session 2). Resolution record:
1. Threshold restored to exactly 0.2 and never touched again (QA P3).
2. Root cause documented in `06_research/physics/virial_theorem.md`:
   (a) the 1-D initial conditions are unphysical for a circular-orbit claim —
   every 1-D bound orbit is a radial plunge whose close approaches are
   unresolved by fixed-dt leapfrog → numerical heating → escape (F10);
   (b) the old test bound integrate()'s 3rd return value (the per-tick virial
   RATIO) to a name `V`, computed "T = E − V", and reported
   mean(E−v̄)/mean(v̄) = Ē/V̄ − 1 ≈ −1.0008 — an algebraic artifact, not data.
3. Test rebuilt on an exactly-derivable 2-D circular orbit (v = 0.25 per body,
   self-consistent G = 1/⟨d²⟩ = 0.25): per-tick AND time-averaged
   |T/V + 0.5| asserted < 0.2; measured deviations ~1e-10.
4. Engine: isotropic (radial) softening ‖dx‖² + ε² for multi-D states
   (enabler; 1-D results bit-identical).
5. Harness: float64 enabled in `tests/conftest.py` — a precision setting for
   I2's 1e-9 threshold, not a threshold change.
6. Generalized virial theorem derived and documented
   (`06_research/physics/generalized_virial.md`); its I≠0, γ≠0 test is
   assigned T-008 in `12_prompts/TaskQueue.md`.
**Evidence:** 9/9 tests pass (2026-10-07); docs cited above.

## CON-003: G fallback constant in degenerate geometry
**Date:** 2026-10-07 (opened by Session-2 audit)
**Files:** `src/physics_jax.py::compute_self_induced_G` vs
`01_foundation/Axioms.md` (Axiom 4)
**Description:** When mean pairwise squared distance < ε (co-located or empty
books), the engine returns G = 1.0 — an unlogged magic constant, structurally
identical to the rejected ADR-007. Physics.md's formula 1/⟨d²⟩ is simply
undefined there. Related spec divergence: Physics.md says G_eff uses a
"running average over recent ticks" while `integrate()` freezes G from the
initial state — two different dynamical systems (see R-PHY-002).
**Severity:** LOW-MEDIUM (no test hits the branch; the frozen-vs-running
divergence blocks the general wording of H2/I2)
**Resolution options (human/ADR decision — Axioms are human-only):**
(a) G = 1/ε (continuous limit of the formula);
(b) G = 0 (co-located ⇒ no gravitational degree of freedom — matches the
    existing "single body ⇒ no gravity" branch);
(c) keep 1.0 and register it as an explicit, justified axiom amendment.
**Status:** OPEN — do not silently change the engine; decide, then update
Physics.md and (if needed) Decisions.md.

## Conflict Resolution Rules
1. If conflict with Philosophy → Philosophy wins.
2. If conflict with Axioms → Axioms wins.
3. If conflict with AI_Protocol → AI_Protocol wins.
4. Otherwise, escalate to human.

## History
| Date | Conflict | Resolution |
|------|----------|------------|
| 2026-10-07 | CON-001: G_DEFAULT violation | ADR-007 rejected |
| 2026-10-07 | CON-002: virial test vs I4 | RESOLVED — test rebuilt on 2-D circular orbit (R-PHY-001), F10 logged, generalized theorem derived |
| 2026-10-07 | CON-003: G fallback 1.0 + frozen-vs-running G | OPEN — ADR decision required (options a/b/c) |
"""

DOCS["08_failures/FailureModes.md"] = r"""# Failure Modes

## F1 — Jump-to-Zero Depth
**Scenario:** Order book depth drops to zero in a single tick.
**Response:** $m \to 0$, $\vec L \to 0$ → freeze.
**Severity:** Low (self-correcting).

## F2 — Cross-Exchange Divergence
**Scenario:** Binance and Coinbase diverge by 5%.
**Response:** Cross-asset gravity pulls toward equilibrium.
**Severity:** Medium (short-term).

## F3 — Exogenous Shock
**Scenario:** Major news event (Fed, hack).
**Response:** Outside L2 field → system blind.
**Severity:** High (unavoidable).

## F4 — Numeric Overflow
**Scenario:** $1/d^3$ as $d \to 0$.
**Response:** $\epsilon$ regularizer.
**Severity:** Low.

## F5 — Detector False Positive
**Scenario:** Iceberg misidentified.
**Response:** Effective mass error.
**Severity:** Low (transient).

## F6 — Tick Drop
**Scenario:** A single tick is lost.
**Response:** Wrong integration step.
**Severity:** Medium.

## F7 — Symplectic Drift
**Scenario:** Cumulative numeric error.
**Response:** Periodic projection onto constraint manifold.
**Severity:** Low.

## F8 — Virial Breakdown
**Scenario:** $T/V$ diverges from $-1/2$.
**Response:** System returns to equilibrium (for conservative subsystem).
**Severity:** Self-healing.
**Clarified 2026-10-07 (R-PHY-001):** per-tick $T/V = -\frac12$ holds only for
circular (≥2-D) orbits; for general eccentricity it holds for *time-averages
over integer periods* ($\langle T\rangle/\langle V\rangle$). A per-tick
deviation inside an elliptical orbit is not a breakdown. "Self-healing" applies
only when the trajectory is collision-resolved (F10) — otherwise the divergence
is a numerical artifact, not dynamics.

## F9 — Generalized Virial Test Failure
**Scenario:** Generalized virial theorem $|2\langle T \rangle + \langle V \rangle + \langle F_{ext} \cdot x \rangle + \langle F_{friction} \cdot x \rangle| > \text{threshold}$.
**Response:** Log as falsification in FailureModes.md. Do NOT loosen threshold.
**Severity:** Varies — may indicate model inadequacy.
**Status:** MONITORED

## F10 — Unresolved Close-Approach Heating (1-D "Orbit" Artifact)
**Added:** 2026-10-07 (Session 2), from R-PHY-001.
**Scenario:** A conservative test (or live 1-D sub-step) with bound
gravitating bodies in 1-D. Zero angular momentum ⇒ every bound orbit is a
radial plunge; separation collapses toward the ε=1e−8 softening core; velocity
spikes (|v| ~ 7e3 analytically at core scale) render the fixed-dt leapfrog
steps unresolved. Discrete-time scattering injects energy (measured:
E −0.115 → +296, pair escapes), and any time-averaged invariant (virial, energy)
computed on that trajectory measures the numerical fireball, not the model.
**Symptoms:** |⟨E⟩ jump| ≫ 1e−9·|E|; virial-like ratios converging to −1 (or
blowing up through the |V| < ε division guard, e.g. means of order −1e5).
**Response:** Do NOT touch thresholds and do NOT "compensate" the ratio. Reject
the *configuration*: any conservative invariant test must pass the
collision-resolution preflight of `06_research/physics/orbital_conditions.md`
(min sep ≥ C·dt·max|v|), or be defined in ≥2-D with an angular-momentum barrier
(circular orbit being the exact case).
**Severity:** HIGH for test validity; zero for the model (theorem survived —
it was the experiment that died).
**Related:** F4 (why ε exists), F8 (correct interpretation), F9, I2/I4.
"""

DOCS["09_agents/AI_Protocol.md"] = r"""# AI Research Protocol

## هدف
این فایل به AI می‌گوید چگونه در پروژه مشارکت کند.

## قواعد تغییرناپذیر
1. هیچ فیلتر، اندیکاتور، یا پارامتر بیرونی اضافه نکن.
2. هیچ مدیریت ریسکی اضافه نکن.
3. هر تغییر در `Decisions.md` ثبت شود.
4. هر فرضیه جدید در `Hypotheses.md` با معیار رد.
5. هر شکست در `FailureModes.md`.

## وظایف AI
1. فاز فعلی roadmap را از `TaskQueue.md` بخوان.
2. یک وظیفه بردار.
3. در `ResearchLog.md` گزارش بده.
4. اگر تعارض دید، در `Conflicts.md` ثبت کن.
5. اگر مسئله حل‌نشده دید، در `OpenProblems.md` اضافه کن.

## خروجی مورد انتظار
- کد در `src/`
- تست در `tests/`
- گزارش در `docs/`
- داده در `data/`

## ممنوعیت‌ها
- تغییر در `Philosophy.md` (فقط انسان).
- تغییر در `Axioms.md` (فقط انسان).
- تغییر در این فایل (فقط انسان).
- ادعای سود واقعی.
- ادعای قابلیت اجرا.

## چک‌لیست هر تغییر
- [ ] آیا پارامتر بیرونی اضافه شد؟ (اگر بله، رد)
- [ ] آیا فیلتر اضافه شد؟ (اگر بله، رد)
- [ ] آیا در Decisions ثبت شد؟
- [ ] آیا تست نوشته شد؟
- [ ] آیا ناورداها حفظ شدند؟

## پروتکل گزارش
هر گزارش در `ResearchLog.md` با فرمت:
```
## [تاریخ] [فاز] [موضوع]
**هدف:**
**روش:**
**نتیجه:**
**گام بعد:**
```

## حالت شکست AI
اگر AI قانونی را زیر پا گذاشت:
1. در `Conflicts.md` ثبت شود.
2. تغییر برگردانده شود.
3. گزارش به انسان.
"""

DOCS["09_agents/AgentHandoff.md"] = r"""# Agent Handoff

> Newest session packet on top; the generic protocol follows below.

---

## Session Packet — 2026-10-07 (Session 2)
**From:** agent-arena (Arena Agent Mode, branch `arena/99b3b317-kepler`)
**To:** next agent / ANY
**Read:** `docs/00_INDEX.md` → `docs/STATE_INVENTORY.md` → this packet. That's the whole 5 minutes.

### 1. What Was Done This Session
- Full state audit (measured, not assumed) — the incoming brief's claims were
  wrong in 3 places; all logged in `docs/ResearchLog.md` + `STATE_INVENTORY.md`.
- Reorganized 47 flat docs into the 12 numbered categories + `00_INDEX.md` +
  `06_research/` registry (git mv history preserved; `generate_docs.py`
  retargeted so regeneration reproduces the tree).
- Resolved R-PHY-001 (virial): the "T/V → −1.0" was a **double artifact** —
  unphysical 1-D radial-plunge ICs (F10: numerical heating −0.115 → +296)
  AND a test assignment bug (`V` actually held integrate()'s ratio output;
  reported ratio was the identity Ē/V̄ − 1 ≈ −1.0008). Circular orbits do not
  exist in 1-D; the brief's recommended "v_circ fix in 1-D" also fails.
- Fixed `src/physics_jax.py`: isotropic multi-D softening, shape-safe
  `acceleration`, consistent imbalance statistic; added `src/__init__.py`.
- Rebuilt `test_virial_ratio_convergence` on a 2-D circular orbit
  (v = √(G·m·r)/d = 0.25; T/V = −0.5 exactly). Thresholds UNTOUCHED (0.2).
- Added `tests/conftest.py` enabling float64 — the only way to meet I2's
  pre-existing 1e−9 threshold in float32-era JAX; precision, not loosening.
- Fixed the previously *unreported* I2 failure (same float64 root cause).
- Opened **CON-003** (G fallback `1.0` + frozen-vs-running G spec divergence) —
  needs a human/ADR decision; do not silently patch the engine.

### 2. Current Test Status (verified this session)
9 total · **9 passing** · 0 failing · 0 skipped (`python -m pytest tests/ -v`).

### 3. Next Session MUST Do
1. `python -m pytest tests/ -v` — trust measurement over any brief.
2. Pick from `06_research/README.md`: **R-PHY-002** (G_eff decision, HIGH —
   gates honest wording of H2/I2) or R-PHY-003 T-009 (preflight helper + dt
   sweep) or T-008 (generalized-virial test for R-PHY-004).
3. If the human passes a decision on CON-003, implement + record in
   `11_meta/Decisions.md`, then update Physics.md.
4. Apply Five Whys if stuck; FMEA before implementation; update AgentSync +
   ResearchLog + STATE_INVENTORY at session end. ALWAYS.

### 4. Critical Constraints (Never Violate)
No filters / indicators / risk-management / external parameters · time = tick ·
never loosen test thresholds (0.2 for I4, 1e−9 for I2 — both proven
attainable now) · Philosophy/Axioms/AI_Protocol are human-only · every failure
gets a FailureModes entry, every decision a Decisions entry.

### 5. Known Blockers
- CON-003 (decision required; engine behavior pinned meanwhile).
- No `pyproject.toml` / CI; environment must be bootstrapped manually:
  `pip install "jax[cpu]" pytest` (float64 comes from `tests/conftest.py`).
- JAX ≥ 0.4 assumed (tested on 0.10.2 / CPU).

### 6. Files Changed This Session
`docs/**` (reorg + new: `00_INDEX.md`, `STATE_INVENTORY.md`, `06_research/**`,
updated FailureModes F10/F8, Conflicts CON-002→RESOLVED/CON-003, Hypotheses H2,
Invariants I2/I4 notes, Physics.md notes, ResearchLog, AgentSync, this packet,
Changelog v0.6.0, TaskQueue T-003/T-004 closed + T-008/T-009 added),
`src/physics_jax.py`, `src/__init__.py` (new), `tests/conftest.py` (new),
`tests/test_physics.py`, `generate_docs.py`.

### 7. Recommended First Actions
```bash
python -m pytest tests/ -v
cat docs/00_INDEX.md
cat docs/06_research/README.md
# then open 06_research/physics/gravity_derivation.md (R-PHY-002)
```

---

# Agent Handoff Protocol

## Purpose
Standardized protocol for transferring work between AI agents.

## Before You Stop

### 1. Update AgentSync.md
- Mark current task as completed or in-progress
- List any blockers
- Note time spent

### 2. Commit All Code
- All code changes committed with clear message
- Tests passing
- No looming conflicts

### 3. Update ResearchLog.md
- Document findings, decisions, and next steps
- Include timestamps

### 4. Update Conflicts.md
- Any open issues clearly documented
- Severity and proposed resolution noted

### 5. Post to Paperclip (if available)
- Summary comment on relevant issue
- Or create document with consolidated knowledge

## When You Start

### 1. Read AgentSync.md Completely
- Know who else is active
- See what tasks are claimed
- Check for recent discoveries

### 2. Check Conflicts.md
- Review all open conflicts
- Understand severity and proposed resolutions
- Don't start work that requires conflict resolution without addressing it

### 3. Read Last 5 ResearchLog Entries
- Catch up on recent work
- Understand decisions made
- Know what's left to do

### 4. Pick a Task from TaskQueue.md
- Choose highest priority unclaimed task
- Claim it in AgentSync.md
- Start working

## Handoff Message Format

When handing off (via Paperclip comment or AgentSync update):

```markdown
## Handoff: [Agent A] → [Agent B]
**Time:** [timestamp]
**Completed:** [list]
**In Progress:** [list]
**Blocked:** [list with reasons]
**Next Priority:** [task ID]
**Notes:** [any context the next agent needs]
```

## Emergency Handoff
If you must stop immediately:
1. Save current work (commit if possible)
2. Update AgentSync.md with "EMERGENCY HANDOFF"
3. List exact file positions and next line to execute
4. Do NOT leave conflicts unresolved
"""

DOCS["09_agents/AgentSync.md"] = r"""# Agent Synchronization

## Session Log (newest first)

### [2026-10-07] Session 2 — COMPLETE
**Agent:** agent-arena
**Duration:** ~1 working session (audit → reorg → research → fix → handoff)
**Tasks Completed:** State audit · docs/ reorg into 12 categories ·
R-PHY-001 resolved (virial) · engine multi-D softening fix · virial test
rebuilt (2-D circular orbit) · float64 harness · CON-002 closed · CON-003
opened (decision needed) · F10 logged · H2 revised.

**Artifacts:**
- `docs/00_INDEX.md`, `docs/STATE_INVENTORY.md` (new)
- `docs/06_research/` (new: README + physics R-PHY-001..004, detectors, MM mapping)
- `docs/09_agents/AgentHandoff.md` (session packet on top)
- `src/physics_jax.py` (fixed), `src/__init__.py`, `tests/conftest.py` (new),
  `tests/test_physics.py` (rebuilt test)
- `docs/ResearchLog.md`, `11_meta/Changelog.md` (v0.6.0), `12_prompts/TaskQueue.md`,
  `generate_docs.py` (retargeted to nested tree)

**Test Status:** 9/9 pass (verified at session end, float64, thresholds untouched)

**Handoff:** Read `docs/09_agents/AgentHandoff.md` packet, then `00_INDEX.md`.
**Next Agent:** R-PHY-002 or T-008/T-009; CON-003 needs a human decision —
do NOT silently change the G fallback.

### [2026-10-07] Session 1 — COMPLETE (with corrections by Session 2)
**Agent:** agent-main — documentation migration.
⚠️ Its sync claims were partly inaccurate (see `STATE_INVENTORY.md`: "all docs
translated" — false; "virial fix attempted" — left suite at 7/9, not 8/9).
Trust the measurements below and the ResearchLog, not session narratives.

## Active Agents
| Agent ID | Session Start | Current Task | Status |
|----------|--------------|--------------|--------|
| agent-main | 2026-10-07 | Phase 0: Documentation Migration | ✅ Complete |
| agent-arena | 2026-10-07 | Session 2: audit + reorg + R-PHY-001 | ✅ Complete (idle — next agent takes over) |

## Task Claims
| Task | Claimed By | Claimed At | Status |
|------|-----------|------------|--------|
| Phase 0 (all) | agent-main | 2026-10-07T10:00 | Done |

## Recent Discoveries
- [2026-10-07T10:45] agent-main: G_DEFAULT violation found, ADR-007 rejected (CON-001)
- [2026-10-07T11:00] agent-main: Virial test needs generalized virial theorem (CON-002)
- [2026-10-07T11:15] agent-main: "All Persian/Korean docs translated to English"
  — **retracted by Session-2 audit**: goal/master_prompt/OpenProblems/Detectors/
  MarketMaking/Experiments/AI_Protocol & co. remain Persian.
- [2026-10-07T11:30] agent-main: Missing coordination files created
- [2026-10-07T14:00] agent-arena: The "virial → −1.0" was a test bug (ratio
  output bound to variable `V`) + 1-D radial-plunge heating (F10); circular
  orbits don't exist in 1-D. Rebuilt on 2-D circular orbit → 9/9 pass.
- [2026-10-07T14:10] agent-arena: I2 threshold unreachable in float32 →
  float64 harness (no threshold change).
- [2026-10-07T14:20] agent-arena: engine softening was per-coordinate in ≥2-D
  → fixed to isotropic ‖dx‖²+ε² (1-D bit-identical).
- [2026-10-07T14:30] agent-arena: CON-003 opened: G fallback 1.0 + frozen-vs-
  running G spec divergence — human ADR decision required.

## Blocked Tasks
- (none physics-side; CON-002 closed 2026-10-07)
- ADR decision on CON-003 → gates R-PHY-002 closure.

## Coordination Rules
1. Before starting a task, check this file and Conflicts.md
2. After completing a task, update this file with findings
3. If blocked, document in Conflicts.md and update this file
4. Every 10 tasks, consolidate knowledge and review

## Handoff
When handing off to another agent:
1. Update status to "Handed off to: [agent ID]"
2. Summarize current state in ResearchLog.md
3. List any blockers in Conflicts.md
"""

DOCS["09_agents/Paperclip_Coordination.md"] = r"""# Paperclip Coordination Protocol

## Purpose
This document defines how multiple AI agents coordinate on the Three-Body HFT project using Paperclip.

## When Paperclip is Available

Use Paperclip tools for coordination:

| Action | Tool | Purpose |
|--------|------|---------|
| Check activity | `issues_list` | See completed/in-progress tasks |
| Claim task | `issues_claim` | Prevent duplicate work |
| Post findings | `comments_create` | Share discoveries |
| Sync context | `documents_create` | Persistent memory |
| Log decisions | `documents_update` | ADR trail |

## Mandatory Sync Protocol

### Before Starting Any Task
1. Query `issues_list` for recent activity
2. Read `AgentSync.md` for manual coordination
3. Check `Conflicts.md` for open issues

### When Claiming a Task
1. Use `issues_claim` with agent ID (if Paperclip available)
2. OR update `AgentSync.md` with claim (manual fallback)

### After Completing a Task
1. Post summary via `comments_create` (Paperclip) or `AgentSync.md` (manual)
2. Update `ResearchLog.md` with findings
3. Update `Changelog.md` if applicable

### Every 10 Tasks
1. Consolidate knowledge in `documents` (Paperclip) or `AgentHandoff.md` (manual)
2. Review all open conflicts
3. Check for duplicated work

## Paperclip Issue Format

When creating issues via Paperclip:
```markdown
**Task:** T-XXX
**Title:** [Short description]
**Description:** [Full task description from TaskQueue.md]
**Agent:** [agent ID]
**Status:** Claimed/In Progress/Complete
**Artifacts:** [file paths created/modified]
**Blockers:** [if any]
```

## Paperclip Document Format

For persistent memory:
```markdown
# [Document Title]

## Created: [timestamp]
## By: [agent ID]
## Purpose: [why this document exists]

## Content: [structured knowledge]
```
"""

DOCS["09_agents/QA_Protocol.md"] = r"""# QA Protocol

## Purpose
This document defines the Quality Assurance workflow for the Three-Body HFT project.

## QA Principles

### P1: Invariant-First
Every code change must preserve all invariants from `Invariants.md`.

### P2: Falsification-First Testing
Tests define rejection criteria. If a test fails, the model (not the test) must be questioned.

### P3: No Threshold Laziness
Test thresholds in `Invariants.md` are fixed. Do not loosen them to make tests pass.

### P4: Reproducibility
All tests must be deterministic and reproducible.

## QA Workflow

### For New Code
1. Write code with type hints and docstrings
2. Write unit tests for all invariants
3. Run tests: `pytest tests/ -v`
4. If all pass: commit with changelog entry
5. If any fail: apply 5 Whys, fix code or reject model

### For Bug Fixes
1. Identify failing invariant
2. Apply 5 Whys to find root cause
3. Fix code (not test threshold)
4. Verify fix with tests
5. Document in ResearchLog.md

### For Refactoring
1. Ensure all tests still pass
2. Verify invariants preserved
3. Update documentation

## Test Categories

### Unit Tests
- Location: `tests/`
- Run with: `pytest tests/ -v`
- Must pass before any commit

### Invariant Tests
- Location: `tests/test_invariants.py` (to be created)
- Test against `Invariants.md`
- Failure = immediate halt

### Integration Tests
- Location: `tests/test_integration.py` (to be created)
- Test cross-module behavior
- Run before major releases

## QA Checklist (per change)
- [ ] All tests pass
- [ ] No invariant violated
- [ ] No threshold loosened
- [ ] Documentation updated
- [ ] ResearchLog updated
- [ ] Changelog updated
- [ ] Decisions updated (if ADR affected)

## CI/CD
When available, automated CI should run:
- `pytest tests/ -v` on every commit
- Block merge if any test fails

## Escalation
If QA cannot be resolved:
1. Document in `Conflicts.md`
2. Notify other agents via `AgentSync.md`
3. Escalate to human if unresolved
"""

DOCS["10_templates/FMEA_Template.md"] = r"""# FMEA Template

## Purpose
Failure Mode and Effects Analysis (FMEA) for systematic risk assessment of new modules.

## When to Use
- Before adding a new physics module
- Before adding a new detector
- Before integrating external data
- After any production bug
- During design review

## FMEA Format

```markdown
## FMEA: [Module Name]

| Failure Mode | Effect | Severity (1-10) | Cause | Occurrence (1-10) | Detection (1-10) | RPN | Action |
|-------------|--------|-----------------|-------|-------------------|------------------|-----|--------|
| [Mode 1] | [Effect] | [1-10] | [Cause] | [1-10] | [1-10] | [S×O×D] | [Action] |
| [Mode 2] | [Effect] | [1-10] | [Cause] | [1-10] | [1-10] | [S×O×D] | [Action] |
```

## Scoring Guide

### Severity (S)
- 1-3: Minor impact, easily tolerated
- 4-6: Moderate impact, workarounds exist
- 7-8: Significant impact, requires attention
- 9-10: Critical impact, system failure

### Occurrence (O)
- 1-3: Rare, < 1% of time
- 4-6: Occasional, 1-10% of time
- 7-8: Frequent, 10-50% of time
- 9-10: Very frequent, > 50% of time

### Detection (D)
- 1-3: Easily detected (tests, logs)
- 4-6: Moderately detectable
- 7-8: Hard to detect
- 9-10: Very hard or impossible to detect

### RPN (Risk Priority Number)
- RPN = Severity × Occurrence × Detection
- RPN > 100: Requires action before proceeding
- RPN > 500: Blocker — do not proceed without fix

## Example: FMEA for physics_jax.py

```markdown
## FMEA: physics_jax.py

| Failure Mode | Effect | Severity | Cause | Occurrence | Detection | RPN | Action |
|-------------|--------|----------|-------|------------|-----------|-----|--------|
| Numeric overflow | NaN in L, crash | 9 | 1/d³ blowup | 8 | 2 | 144 | Epsilon softening (implemented) |
| Energy drift | Violated I2 | 7 | Large dt | 6 | 3 | 126 | Use adaptive dt or verify with tests |
| Zero mass division | NaN in acceleration | 8 | Empty book | 5 | 4 | 160 | Guard with jnp.where (implemented) |
| JAX tracing error | Runtime error | 7 | Python if on traced array | 6 | 5 | 210 | Use jnp.where instead of if (implemented) |
| Pytree registration missing | JIT failure | 8 | Forgot registration | 4 | 3 | 96 | Register on class definition (implemented) |
```

## Action Thresholds

- **RPN > 100:** Must document mitigation in code comments
- **RPN > 200:** Must implement fix before merging
- **RPN > 500:** Cannot proceed — redesign required

## Post-FMEA Checklist
- [ ] All failure modes identified
- [ ] RPN calculated for each
- [ ] Actions documented for RPN > 100
- [ ] Fixes implemented for RPN > 200
- [ ] FMEA recorded in ResearchLog.md
"""

DOCS["10_templates/Five_Whys_Template.md"] = r"""# Five Whys Template

## Purpose
Root cause analysis protocol for debugging test failures, bugs, or unexpected behavior.

## When to Use
- Test fails unexpectedly
- Bug appears in production code
- Invariant violation detected
- Behavior doesn't match model prediction

## Protocol

Apply 5 Whys iteratively:

```markdown
## 5 Whys Analysis: [Problem Description]

**Problem:** [Clear, specific statement of the observed issue]

**Why 1:** [First answer — direct cause]
**Why 2:** [Deeper cause — why did Why 1 happen?]
**Why 3:** [Deeper cause — why did Why 2 happen?]
**Why 4:** [Deeper cause — why did Why 3 happen?]
**Why 5:** [Root cause — why did Why 4 happen?]

**Root Cause:** [Confirmed technical or systemic cause]
**Fix:** [Action taken to address root cause]
**Verification:** [How you verified the fix works]
```

## Rules

1. **Focus on process, not blame.** The goal is to fix the system, not assign fault.

2. **Branch when needed.** If a single chain doesn't reach root cause, branch into multiple paths:
   ```markdown
   **Branch A:** [path 1]
   **Branch B:** [path 2]
   ```

3. **Document each step.** Write the analysis in `ResearchLog.md` under a dedicated section.

4. **Stop at actionable root cause.** Don't continue past the point where you can take action.

## Example

```markdown
## 5 Whys Analysis: Energy drift in symplectic integrator

**Problem:** Energy drift of 1e-3 observed over 1000 ticks, expected < 1e-6.

**Why 1:** The integrator is not conserving energy to expected precision.
**Why 2:** The time step dt=0.01 is too large for the system dynamics.
**Why 3:** The gravitational forces are large due to close body proximity.
**Why 4:** G_DEFAULT = 1e-6 amplifies forces at small separations.
**Why 5:** G_DEFAULT is a magic constant, not self-derived from system geometry.

**Root Cause:** Use of magic G_DEFAULT constant violates Axiom 4 (self-induced gravity).

**Fix:** Replace G_DEFAULT with G_eff = 1 / <d²>_t (self-derived from system).

**Verification:** Re-run energy conservation test with G_eff. Expected drift < 1e-6.
```

## Template for ResearchLog.md

```markdown
## [YYYY-MM-DD] [5 Whys] [Problem Title]

**Problem:** [description]

**Why 1:** [answer]
**Why 2:** [answer]
**Why 3:** [answer]
**Why 4:** [answer]
**Why 5:** [answer]

**Root Cause:** [cause]
**Fix:** [action]
**Verification:** [method]
```
"""

DOCS["11_meta/Changelog.md"] = r"""# Changelog

## v0.6.0 — 2026-10-07 (Session 2: audit, doc reorg, virial resolution)
- Audit: measured 7/9 tests at session start (brief claimed 8/9); unreported
  I2 float32 failure found; three inherited claims corrected (ResearchLog).
- `docs/` reorganized into 12 numbered categories; new `00_INDEX.md`,
  `STATE_INVENTORY.md`, `06_research/` registry (R-PHY-001..004,
  R-DET-001/002, R-MM-001); `generate_docs.py` retargeted to the nested tree.
- `src/physics_jax.py`: isotropic (radial) ε-softening for multi-D states in
  `compute_potential_energy` / `acceleration` / `compute_self_induced_G`;
  shape-safe `acceleration`; consistent `max|I|` initial imbalance statistic.
  1-D numerics unchanged (bit-identical).
- `tests/test_physics.py`: `test_virial_ratio_convergence` rebuilt on a 2-D
  circular orbit with exact v_circ derivation; per-tick AND averaged I4 check;
  former −1.0 root-caused as assignment bug + radial-plunge heating (F10);
  thresholds untouched. Test header documents float64 requirement.
- `tests/conftest.py`: enable JAX float64 (precision for 1e−9 class bounds).
- `src/__init__.py`: package marker.
- Docs: FailureModes +F10 (F8 clarified); Conflicts CON-002 RESOLVED,
  CON-003 OPEN (G fallback magic 1.0; frozen-vs-running G); Hypotheses H2
  revised; Invariants I2/I4 scoped; Physics.md numerical-requirements section;
  TaskQueue T-003/T-004 completed, T-008/T-009 added.
- Status: **9/9 tests pass.**

## v0.1.0 — 2025-01
- Initial Concept, Philosophy, Strategy.

## v0.2.0 — 2025-01
- Added Implementation.
- Introduced physics_jax.

## v0.3.0 — 2025-01
- Added detectors_numba.
- Added market_maker (A-S).

## v0.4.0 — 2025-01
- Migrated to uvloop + orjson.
- Added fast_l2_client.

## v0.5.0 — 2025-01
- Ten L2 states.
- simulation_live_v3.

## v1.0.0 — (target)
- 10 million ticks.
- Full validation.
- Whitepaper.

## [2026-10-07] — physics_jax.py
- Implemented `symplectic_step` (velocity Verlet)
- Implemented `integrate` with lax.scan
- JAX pytree registration for ThreeBodyState
- Invariant tests: energy, angular momentum, virial, imbalance
- Zero-mass (empty book) support without NaN

## [2026-10-07] — Documentation Migration
- Translated all Persian/Korean documentation to English
- Rejected ADR-007 (G_DEFAULT violates Axiom 4)
- Added self-induced gravity formula to Physics.md
- Created coordination files (AgentSync, AgentHandoff, QA_Protocol, etc.)
"""

DOCS["11_meta/Decisions.md"] = r"""# Decisions (ADR)

## ADR-001: Microprice Selection Over Mid
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Microprice is sensitive to order flow imbalance.
**Rejected alternative:** mid (blind to volume).

## ADR-002: JAX for Physics
**Date:** 2025-01
**Status:** Accepted
**Rationale:** JIT + x64 + vmap.
**Rejected alternative:** NumPy (slow), PyTorch (heavy).

## ADR-003: numba for Detection
**Date:** 2025-01
**Status:** Accepted
**Rationale:** 100x faster than pure Python.
**Rejected alternative:** Cython (complex).

## ADR-004: uvloop + orjson
**Date:** 2025-01
**Status:** Accepted
**Rationale:** 2-10x faster.
**Rejected alternative:** asyncio + json (slow).

## ADR-005: No Risk Management
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Risk solved by geometry.
**Rejected alternative:** stop-loss, position limit.

## ADR-006: Time = Tick
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Natural quantization of markets.
**Rejected alternative:** seconds, candles.

## ADR-007: G_DEFAULT = 1e-6 for log-price positions
**Date:** 2026-10-07
**Status:** REJECTED
**Rationale:** VIOLATES Axiom 4 (self-induced gravity without free parameters).
**Rejected alternative:** N/A — this ADR is rejected.
**Rejection rationale:** See CON-001 in Conflicts.md. G must be self-derived from the system geometry, not a magic constant.
**Post-rejection action:** G_eff = 1 / <d²>_t (time-averaged squared distance).
"""

DOCS["11_meta/PriorArt.md"] = r"""# Prior Art

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
"""

DOCS["11_meta/Project_History.md"] = r"""# Project History (consolidated)

> Condensed narrative; the primary records are `docs/ResearchLog.md` (top =
> newest) and `11_meta/Changelog.md`.

## Phase 0 — Genesis (2025-01)
Concept of a three-body "gravity of the order book" mathematical game;
Philosophy/Axioms/Concept and the full documentation tree generated by
`generate_docs.py` (originally Persian; 41+ files). Strategy/detector/MM docs
from this phase remain partly Persian and partly superseded — several of their
formulas (z-scores, seconds-based lifetimes, magic constants) violate the
project's own axioms and are being re-derived in `06_research/`.

## Phase 1 — Data plane (target in roadmap; never implemented in repo)
`fast_l2_client`, tick buffer, Parquet storage (T-001/T-002). Not started in
this repository — docs exist, code does not.

## Phase 2 — physics_jax (2026-10-07)
`src/physics_jax.py`: ThreeBodyState pytree, self-induced G (Axiom 4),
velocity-Verlet `symplectic_step`, `lax.scan` `integrate`; `tests/test_physics.py`
with 9 invariant tests. Session 1 events:
- ADR-007 (`G_DEFAULT = 1e-6`) introduced, then REJECTED → CON-001 resolved;
  engine switched to `G_eff = 1/⟨d²⟩`.
- English translation pass over docs (incomplete: goal/prompt/OpenProblems/
  Detectors/MarketMaking/etc. still Persian — see STATE_INVENTORY).
- Virial test left failing at "T/V → −1.0" (→ CON-002, left OPEN).

## Phase 2b — Audit, reorg, virial resolution (2026-10-07, Session 2)
- Audit: 7/9 tests passed (not 8/9); several inherited claims in the handoff
  brief did not match the repo (no `src/__init__.py`; "F5 = virial failure"
  wrong; I2 failure unreported).
- `docs/` reorganized into 12 numbered categories + `00_INDEX.md`,
  `STATE_INVENTORY.md`, `06_research/` registry; generator retargeted.
- CON-002 resolved: the −1.0 "virial" was a 1-D radial-plunge setup
  (no circular orbits exist in 1-D) compounded by a test assignment bug;
  engine multi-D softening fixed to isotropic; test rebuilt on a 2-D circular
  orbit; float64 enabled for harness (thresholds untouched). 9/9 pass.
- New failure mode F10 (unresolved close-approach numerical heating in 1-D);
  H2 revised; CON-003 opened (G fallback magic value).

## Not (yet) existing
Market-maker code, detectors code, simulation harnesses, CI, packaged deps.
Every doc claiming a phase "Complete" that has no code is a plan, not a state —
`STATE_INVENTORY.md` is the only state authority.
"""

DOCS["11_meta/References.md"] = r"""# References

## Market Microstructure
1. Avellaneda, M., & Stoikov, S. (2008). High-frequency trading in a limit order book. *Quantitative Finance*.
2. Cont, R., Kukanov, A., & Stoikov, S. (2014). The price impact of order book events. *Journal of Financial Econometrics*.
3. Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and High-Frequency Trading*. Cambridge.

## Physics
4. Goldstein, H., Poole, C., & Safko, J. (2002). *Classical Mechanics*. Addison-Wesley.
5. Arnold, V. I. (1989). *Mathematical Methods of Classical Mechanics*. Springer.
6. Chenciner, A., & Montgomery, R. (2000). A remarkable periodic solution of the three-body problem. *Annals of Mathematics*.

## Differential Geometry
7. do Carmo, M. P. (1992). *Riemannian Geometry*. Birkhäuser.
8. Hamilton, R. S. (1982). Three-manifolds with positive Ricci curvature. *Journal of Differential Geometry*.

## Gauge Theory
9. Nakahara, M. (2003). *Geometry, Topology and Physics*. IoP.
10. Peskin, M., & Schroeder, D. (1995). *An Introduction to QFT*. Addison-Wesley.

## Statistical Methods
11. Hawkes, A. G. (1971). Spectra of some self-exciting point processes. *Biometrika*.
12. Benford, F. (1938). The law of anomalous numbers. *Proceedings of the American Philosophical Society*.

## Complexity
13. Mandelbrot, B. (1963). The variation of certain speculative prices. *Journal of Business*.
14. Sornette, D. (2003). *Why Stock Markets Crash*. Princeton.
"""

DOCS["11_meta/goal.md"] = r"""# Goal

## هدف اصلی
اثبات یا رد این فرضیه:
> **آیا هندسه سه‌جسمی می‌تواند میکروساختار بازار L2 را توصیف کند؟**

## اهداف فرعی

### G1 — مدل‌سازی
ساخت یک مدل ریاضی که در آن:
- جرم از عمق L2 می‌آید
- نیرو از عدم توازن
- اصطکاک از اسپرد
- هج از نسبت جرم
- گرید از سطوح واقعی

### G2 — شبیه‌سازی
اجرای ۱۰ میلیون tick روی BTC/ETH/SOL و ثبت نتایج.

### G3 — اعتبارسنجی
تست ۷ فرضیه با معیار رد مشخص.

### G4 — مستندسازی
تولید یک کاغذ سفید ریاضی.

## اهداف غیر-هدف

- ❌ سود واقعی
- ❌ اجرای زنده
- ❌ فروش استراتژی
- ❌ جذب سرمایه

## معیارهای موفقیت

### کوتاه‌مدت (۱ ماه)
- [ ] T-001 تا T-004 کامل
- [ ] ۱۰۰٬۰۰۰ tick شبیه‌سازی
- [ ] ‖L‖ کران‌دار

### میان‌مدت (۳ ماه)
- [ ] ۱۰M tick
- [ ] Π > 0 با CI 95%
- [ ] ۷ فرضیه تست‌شده

### بلندمدت (۶ ماه)
- [ ] Whitepaper
- [ ] انتشار arXiv
- [ ] نظریه واحد

## چه چیزی این پروژه را موفق می‌کند؟
اگر بتوانیم نشان دهیم:
$$
\text{Orbit} = \text{Market Microstructure}
$$
با معیارهای قابل تست.

## چه چیزی این پروژه را شکست می‌دهد؟
- اگر L پایسته نباشد.
- اگر سود منفی باشد.
- اگر فریز خودکار کار نکند.
- اگر تطبیق در ۱۰ حالت شکست بخورد.

## اصل راهنما
> **حقیقت مهم‌تر از سود است. رد شدن هم یک نتیجه است.**
"""

DOCS["12_prompts/PromptLibrary.md"] = r"""# Prompt Library

## پرامپت‌های استاندارد

### P1 — برداشتن وظیفه
```
وظیفه بعدی را از TaskQueue.md بردار.
فاز فعلی و وابستگی‌ها را چک کن.
اگر همه پیش‌نیازها برآورده شده، شروع کن.
در ResearchLog.md گزارش بده.
```

### P2 — تست فرضیه
```
Hypotheses.md را بخوان.
یک فرضیه قابل رد انتخاب کن.
Experiment مربوطه را در Experiments.md طراحی کن.
کد تست بنویس در tests/.
نتیجه را در ResearchLog.md ثبت کن.
اگر رد شد، در FailureModes.md اضافه کن.
```

### P3 — افزودن فاز جدید
```
roadmap.md را بخوان.
فاز بعدی را بردار.
پیش‌نیازها را چک کن.
یک وظیفه در TaskQueue.md اضافه کن.
```

### P4 — بررسی تعارض
```
همه فایل‌های docs/ را اسکن کن.
هر تناقض را در Conflicts.md ثبت کن.
پیشنهاد حل بده.
```

### P5 — بررسی ناورداها
```
Invariants.md را بخوان.
هر ناوردا را با کد تست کن.
اگر شکست خورد، علت را در FailureModes.md بنویس.
```

### P6 — بهینه‌سازی
```
hot path ها را پیدا کن (profiling).
اگر کند است، از numba/JAX استفاده کن.
بدون تغییر در رفتار، فقط سرعت.
```

### P7 — بسط ریاضی
```
OpenProblems.md را بخوان.
یک مسئله انتخاب کن.
بسط ریاضی بده.
اگر ثابت شد، به Concept.md اضافه کن.
اگر رد شد، در FailureModes.md ثبت کن.
```

### P8 — بازبینی
```
آخرین تغییرات را از Changelog.md بخوان.
آیا با Philosophy.md سازگارند؟
اگر نه، در Conflicts.md ثبت کن.
```
"""

DOCS["12_prompts/TaskQueue.md"] = r"""# Task Queue

## Status: Active

## Open

### T-001 [Phase 1] [High]
- **Title:** Implement fast_l2_client.py
- **Input:** DataSpec.md
- **Output:** WebSocket client
- **Criterion:** Receive 10,000 ticks without dropout

### T-002 [Phase 1] [High]
- **Title:** tick_buffer with polars
- **Input:** DataSpec.md
- **Output:** Parquet storage
- **Criterion:** Deterministic retrieval

### T-003 [Phase 2] [High]
- **Title:** physics_jax.py
- **Input:** Physics.md
- **Output:** symplectic_step
- **Criterion:** Angular momentum conservation to 1e-9

### T-004 [Phase 2] [Medium]
- **Title:** Invariant tests
- **Input:** Invariants.md
- **Output:** tests/test_physics.py
- **Criterion:** All pass

### T-005 [Phase 3] [High]
- **Title:** detectors_numba.py
- **Input:** Detectors.md
- **Output:** Iceberg + Spoof
- **Criterion:** F1 > 0.8 on synthetic data

### T-006 [Phase 4] [High]
- **Title:** market_maker.py
- **Input:** MarketMaking.md
- **Output:** quote_all
- **Criterion:** bid < ask always

### T-007 [Phase 5] [High]
- **Title:** simulation_live_v3
- **Input:** All
- **Output:** 10M tick simulation
- **Criterion:** Pi > 0 with 95% CI

### New (Session 2, 2026-10-07)

### T-008 [Phase 2] [High]
- **Title:** Generalized virial identity test (I≠0, γ≠0)
- **Input:** `06_research/physics/generalized_virial.md` (derivation done)
- **Output:** `tests/test_physics.py::test_generalized_virial_identity`
- **Criterion:** |2⟨T⟩+⟨V⟩+⟨Σ mᵢIᵢxᵢ⟩−⟨Σ γᵢ|vᵢ|²⟩| / |⟨V⟩| < 0.2 over exact
  integer periods, config passes R-PHY-003 preflight. Failure → F9 falsification.

### T-009 [Phase 2] [Medium]
- **Title:** Collision-resolution preflight + dt/eccentricity sweep (R-PHY-003)
- **Input:** `06_research/physics/orbital_conditions.md`
- **Output:** shared test helper + sweep table
- **Criterion:** helper rejects the historical F10 configs; sweep boundary
  documented.

### T-010 [Phase 2] [Blocking decision]
- **Title:** CON-003 adjudication (G fallback; frozen-vs-running G) — HUMAN/ADR
- **Input:** `06_research/physics/gravity_derivation.md`, `08_failures/Conflicts.md`
- **Output:** ADR-008 + Physics.md alignment (+ engine change if decided)

## In Progress
(Empty)

## Completed
- [x] T-000 [Phase 0] Generate all docs
- [x] T-003 [Phase 2] physics_jax.py + symplectic_step — L conserved to 1e−14
      in float64 (criterion 1e−9 met; Session 2, multi-D softening fix included)
- [x] T-004 [Phase 2] Invariant tests — 9/9 pass; CON-002 resolved;
      F10 documented (Session 2, 2026-10-07)

## Prioritization
1. T-010 (decision — unblocks honest generalization of H2/I2), then T-008, T-009 (physics research)
2. T-001, T-002 (infrastructure)
3. T-005 (detection; gated by R-DET-001/002 formalization)
4. T-006 (MM; gated by R-MM-001 audit)
5. T-007 (integration)
Completed: T-003, T-004 (physics core) — 9/9 tests.
"""

DOCS["12_prompts/master_prompt.md"] = r"""# Master Prompt

## نقش
تو یک پژوهشگر ریاضی هستی که روی پروژه «سه‌جسمی HFT» کار می‌کند.

## هدف
اثبات یا رد اینکه هندسه سه‌جسمی می‌تواند میکروساختار L2 را توصیف کند.

## ورودی
تمام فایل‌های `docs/`.

## قواعد تغییرناپذیر
1. **هیچ فیلتر.** هیچ اندیکاتور.
2. **هیچ مدیریت ریسکی.** ریسک در قید هندسی.
3. **هیچ پارامتر بیرونی.** همه از داده.
4. **زمان = tick.**
5. **این پروژه هرگز اجرا نمی‌شود.**

## جریان کار

### گام ۱ — خواندن
- `Philosophy.md` (چرا)
- `Axioms.md` (اصول)
- `Concept.md` (چیست)
- `TaskQueue.md` (چه کاری)

### گام ۲ — انتخاب
- یک وظیفه از `TaskQueue.md` بردار
- وابستگی‌ها را چک کن
- اگر پیش‌نیاز نیست، صبر کن

### گام ۳ — اجرا
- کد در `src/`
- تست در `tests/`
- مستندسازی در `docs/`

### گام ۴ — اعتبارسنجی
- `Invariants.md` را چک کن
- `Hypotheses.md` را تست کن
- اگر شکست خورد → `FailureModes.md`

### گام ۵ — گزارش
- `ResearchLog.md` را به‌روز کن
- `Changelog.md` را به‌روز کن
- `Decisions.md` را به‌روز کن

## خروجی مورد انتظار
هر تغییر باید شامل:
1. کد
2. تست
3. گزارش
4. به‌روزرسانی docs

## ممنوعیت مطلق
- ❌ استفاده از pandas در hot path
- ❌ `time.sleep` در حلقه اصلی
- ❌ `threading.Lock`
- ❌ حافظه unbounded
- ❌ پارامتر magic
- ❌ ادعای سود
- ❌ ادعای اجرا

## سبک کد
- Python 3.10+
- Type hints
- Docstring برای هر تابع
- تست unit اجباری
- نام‌گذاری واضح

## سبک مستندسازی
- Markdown
- فرمول با LaTeX (`$...$` یا `$$...$$`)
- جدول برای مقایسه
- مثال عددی

## اگر گیر کردی
1. `OpenProblems.md` را چک کن
2. `Conflicts.md` را چک کن
3. اگر حل نشد → به انسان ارجاع

## چک‌لیست قبل از commit
- [ ] همه تست‌ها pass
- [ ] ناورداها حفظ
- [ ] پارامتر بیرونی اضافه نشده
- [ ] فیلتر اضافه نشده
- [ ] مستندات به‌روز
- [ ] ResearchLog به‌روز

## نمونه پرامپت اجرا

```
# فعال‌سازی AI

۱. docs/Philosophy.md را بخوان.
۲. docs/Axioms.md را بخوان.
۳. docs/TaskQueue.md را بخوان.
۴. اولین وظیفه باز با اولویت بالا را بردار.
۵. پیاده‌سازی کن.
۶. تست کن.
۷. ResearchLog.md را به‌روز کن.
۸. برگرد به گام ۴.
```

## نمونه پرامپت بسط نظری

```
# بسط نظری

۱. docs/OpenProblems.md را بخوان.
۲. یک مسئله انتخاب کن.
۳. برای آن راه‌حل ریاضی بنویس.
۴. اگر ثابت شد → Concept.md را به‌روز کن.
۵. اگر رد شد → FailureModes.md را به‌روز کن.
۶. اگر ناتمام → OpenProblems.md را به‌روز کن.
۷. ResearchLog.md را بنویس.
```

## نمونه پرامپت اعتبارسنجی

```
# اعتبارسنجی

۱. docs/Hypotheses.md را بخوان.
۲. docs/Experiments.md را بخوان.
۳. یک آزمایش انتخاب کن.
۴. کد تست بنویس.
۵. اجرا کن.
۶. نتیجه را در ResearchLog.md ثبت کن.
۷. اگر فرضیه رد شد → FailureModes.md.
۸. اگر تأیید شد → Changelog.md.
```

## نکته نهایی
> **هدف این پروژه حقیقت است، نه سود.**
> **رد شدن یک فرضیه = موفقیت پروژه.**
> **هر تغییر باید ردپذیر باشد.**
"""

DOCS["ResearchLog.md"] = r"""# Research Log

## [2026-10-07] [Session 2] [Audit + Doc Reorg + Virial Resolution]

**Goal:** Audit prior session's claimed state, reorganize `docs/` into 12 numbered
categories, resolve CON-002 / the failing virial test, and leave a handoff packet.

**Audit findings (measured, not assumed):**
- Test suite at session start: **7 pass / 2 fail** — the incoming brief claimed 8/9.
  The second, unreported failure was `test_energy_conservation_relative_drift`
  (I2: drift 8e−8 vs threshold 1e−9 → JAX float32 precision limit, *not* an
  integrator bug).
- `src/__init__.py` did **not** exist despite the brief claiming it was created.
- Brief's "F5 = virial failure" was wrong; FailureModes F5 is the detector
  false-positive mode. Real mapping: virial issue = F8, now made precise as F10.
- New finding (F10 + test bug): **the reported "−1.0008 virial ratio" was two
  compounding artifacts, not a model falsification.**
  (A) The old test bound integrate()'s *third return value* (per-tick ratio
  T/V) to a variable named `V`, computed `T := E − V`, and divided the means —
  so "−1.0008" = Ē/V̄ − 1, an algebraic echo; the guarded division (V := ε when
  |V| < ε) after the pair escaped produced the |means| ~ 4e5 magnitudes.
  (B) The 1-D ICs themselves are unphysical for a virial test: every bound
  1-D orbit is a radial plunge (zero angular momentum ⇒ no centrifugal
  barrier); close approaches at dt = 1e−3 are unresolved → numerical heating
  (E: −0.115 → +296). The handoff's recommended "set v = v_circ in 1-D" fix
  was checked and **fails identically** (E: −0.0625 → +160): circular orbits
  do not exist in 1-D at all.
- Engine bug found while diagnosing: multi-D potential/force used per-coordinate
  softening `sqrt(dx_k² + ε²)` instead of radial `sqrt(‖dx‖² + ε²)`, which breaks
  any ≥2-D configuration.
- `integrate()` recorded the initial imbalance as `‖I‖₂` but per-tick values as
  `max|I|` — inconsistent statistic.

**Actions:**
- Reorganized `docs/` (47 flat files) into 12 numbered folders + root
  `00_INDEX.md` / `STATE_INVENTORY.md` / `ResearchLog.md`; created `06_research/`
  with per-topic files (R-PHY-001..004, R-DET-001/002, R-MM-001). `generate_docs.py`
  retargeted so regeneration reproduces the new tree.
- `src/physics_jax.py`: isotropic (radial) softening in `compute_potential_energy`,
  `acceleration`, `compute_self_induced_G`; `zeros_like` shape fix; consistent
  `max|I|` statistic in `integrate` history init. 1-D results unchanged bit-for-bit.
- `tests/conftest.py`: enable `jax_enable_x64` (precision requirement of I2/I4,
  thresholds untouched — QA_Protocol P3 respected).
- `tests/test_physics.py`: virial test rebuilt on a 2-D circular orbit with
  self-consistent v_circ; asserts per-tick AND time-averaged |T/V + 0.5| < 0.2
  (unchanged threshold), L bounded, ratios finite.
- `src/__init__.py` created.

**Result:**
- **9/9 tests pass** (measured at session end; thresholds never changed:
  I4 kept at 0.2, I2 kept at 1e−9 — both now genuinely satisfied).
- R-PHY-001 RESOLVED with full write-up (`06_research/physics/virial_theorem.md`):
  exact 2-D circular orbit gives |⟨T/V⟩ + 0.5| = 1.2e−10 and per-tick ratio
  −0.5 constant; the corrected root cause is *two* bugs — (B) 1-D
  radial-plunge ICs heating E −0.115 → +296 (verified also for v = v_circ:
  −0.0625 → +160), and (A) the old test's assignment bug binding integrate()'s
  ratio output to `V`, making its reported −1.0008 the algebraic echo Ē/V̄ − 1.
- Bonus theorem-check: ⟨T⟩/⟨V⟩ = −0.5 ± 1e−7 for eccentricities to e ≈ 0.75
  when averaged over **exact integer Kepler periods** (dt = 2e−5, 1–10 periods)
  — the virial theorem holds; the old test measured neither theory nor orbit.
- CON-002 closed; CON-003 opened (G fallback 1.0; frozen-vs-running G) —
  needs human ADR. F10 added to FailureModes. H2 revised.

**Next:** R-PHY-002 (G_eff running-average vs frozen-initial spec divergence),
R-PHY-003 sweep table (v/v_circ vs ⟨T⟩/⟨V⟩ vs energy drift).

---

## [2025-01-15] [Phase 0] [Initialization]

**Goal:** Generate complete documentation structure.

**Method:** Generate 41 MD files via script.

**Result:** All files ready.

**Next:** Start T-001.

---

## [2026-10-07] [Phase 2] [physics_jax — Initial Implementation]

**Goal:** Implement three-body physics engine with symplectic integrator (velocity Verlet) in JAX.

**Method:**
- Create `ThreeBodyState` class with position, velocity, mass, imbalance, friction
- Define kinetic energy, potential energy, virial ratio, angular momentum functions
- Implement `symplectic_step` with equations of motion from Concept.md §3
- Implement `integrate` with `lax.scan` for long simulations
- Register ThreeBodyState as JAX pytree for JIT compatibility

**Result:**
- 9 unit tests passing: energy conserved (absolute drift < 1e-5), angular momentum bounded, virial ratio acceptable, imbalance always in [-1,1], zero-mass state frozen without NaN
- Bug fixes: kinetic energy formula, acceleration shape, JAX tracing with zero mass, initial state recording
- G_DEFAULT = 1e-6 for log-price position scale (later rejected — see Conflicts.md)

**Falsifications:**
- H2 virial test initially failed; later found to be a test design issue (see Conflicts.md CON-002)

**Next:**
- T-004: More invariant tests with varied scenarios
- T-001/T-002: WebSocket client and Parquet storage

---

## [2026-10-07] [Phase 0] [Documentation Migration]

**Goal:** Translate all Persian/Korean documentation to English, reject ADR-007, fix virial test.

**Method:**
- Full rewrite of ResearchLog.md, Decisions.md, Changelog.md to English
- Reject ADR-007 in Decisions.md (violates Axiom 4)
- Log G_DEFAULT violation in Conflicts.md as CON-001
- Update Physics.md with self-induced gravity formula
- Create missing coordination files (AgentSync.md, AgentHandoff.md, QA_Protocol.md, Paperclip_Coordination.md, Five_Whys_Template.md, FMEA_Template.md)

**Result:**
- All documentation now in English
- ADR-007 rejected, CON-001 logged
- Self-induced gravity formula documented in Physics.md
- Missing files created

**Next:** Continue with Phase 0.3 (virial test fix)
"""

DOCS["STATE_INVENTORY.md"] = r"""# Kepler State Inventory

> Living file. Every agent reads this BEFORE acting and updates it AFTER acting.
> Pair with `09_agents/AgentSync.md`. Do not trust session prompts or chat
> memory — trust this file and the tests.

## Last Updated: 2026-10-07 (Session 2, end-of-session state)

## Test Status (measured at session end, `python -m pytest tests/ -v`)
- Total: 9 · **Passing: 9** · Failing: 0 · Skipped: 0
- Thresholds are exactly those of `07_hypotheses/Invariants.md` (I4: 0.2,
  I2: 1e−9) — never loosened (QA_Protocol P3). float64 via `tests/conftest.py`
  is a *precision requirement*, documented there.
- At Session-2 start the measured state was **7/9** (the incoming brief's
  "8/9" was wrong; the extra failure was the float32-limited I2 test).

## Files
| Path | Status | Purpose | Note |
|------|--------|---------|------|
| `src/physics_jax.py` | active | Physics engine (velocity Verlet, self-induced G) | 2026-10-07: isotropic multi-D softening, shape-safe acceleration, consistent imbalance statistic; 1-D numerics bit-identical |
| `src/__init__.py` | active | package marker | added Session 2 |
| `tests/test_physics.py` | active | 9 invariant tests | virial test = 2-D circular orbit (exact −0.5); history in docstring + F10 |
| `tests/conftest.py` | active | enables JAX float64 for the suite | required for I2/I4-class thresholds |
| `docs/00_INDEX.md` | active | master entry point | every agent starts here |
| `docs/ResearchLog.md` | active | chronological log, newest first | Session 2 entry = full audit |
| `docs/06_research/` | active | per-topic research (R-XXX-### registry in README) | R-PHY-001 ✅, 002/003/004 open/partial |
| `generate_docs.py` | active | doc generator: DOCS dict ↔ `docs/` tree | regenerate to verify: `python generate_docs.py --out /tmp/docs_check && diff -r docs /tmp/docs_check --exclude=.git` |
| `docs/<NN>_*/` | active | 12 numbered categories (47+3 docs) | reorganized 2026-10-07 via git mv |

## Environment (measured)
- Python 3.11.2 · jax 0.10.2 (CPU) · pytest 9.1.1 · numpy
- Bootstrap: `pip install "jax[cpu]" pytest` (sandbox needed `--break-system-packages`)
- No `pyproject.toml`, no CI, no dependency pins — future work.

## Known Issues & Open Items
- **CON-003 (OPEN, needs human ADR):** `compute_self_induced_G` returns magic
  `G = 1.0` in degenerate geometry; and `integrate()` freezes G from t=0 while
  Physics.md claims a running average — two different dynamical systems.
  Options (a/b/c) recorded in `08_failures/Conflicts.md`. Do not silently patch.
- **F10 (logged):** 1-D conservative configurations cannot satisfy any
  collision-resolved invariant test (radial plunge → numerical heating).
  All future conservative tests must pass the preflight described in
  `06_research/physics/orbital_conditions.md`.
- CON-001 ✅ resolved (Session 1); CON-002 ✅ resolved (Session 2, R-PHY-001).
- Legacy Persian docs kept verbatim: `11_meta/goal.md`,
  `12_prompts/master_prompt.md`, `06_research/open_problems.md`, plus the
  pre-protocol formulas inside `04_market/Detectors.md` / `MarketMaking.md` /
  `07_hypotheses/Experiments.md` — these contain spec content that VIOLATES
  current axioms (z-scores, seconds, magic constants); re-derivation is
  scoped in `06_research/detectors/*` and `06_research/market_making/*`.
  Earlier sync claim "all docs translated" was false.

## Open Questions (physics)
- Which reading of Axiom 4 governs: frozen-initial G (conservative, testable)
  or running-average G (adaptive, non-conservative)? → R-PHY-002 / T-010.
- Is `G = 1/⟨d²⟩` self-consistent off-circular orbits? (For a single pair it
  makes V ∝ −1/d³ effectively — homogeneity exponent n = −3 ⇒ time-averaged
  ratio −3/2, not −1/2. Circular orbits hide this because ⟨d²⟩ = d².) Needs
  an explicit experiment → R-PHY-002 E1.
- Can the generalized four-term identity (R-PHY-004) survive ε-guard and
  softening corrections at realistic tick dt? → T-008.

## Verified This Session (numbers worth reusing)
- 2-D circular orbit (m=1, d=2, G=0.25, v=0.25/body): T = 0.0625,
  V = −0.125, T/V = −0.5 exactly; leapfrog deviation ~1e−10; E drift ~5e−14;
  L = 0.5 constant to 1e−14.
- Eccentric exact-integer-period averages (dt = 2e−5): deviation from −0.5:
  k=0.95 → 5e−10 · k=0.9 → 3e−8 · k=0.8 → 7e−8 (1 period), 2e−9 (10 periods);
  k=0.6 → 1.4e−7 · k=0.5 → 7.4e−8. Escape boundary v/v_circ = √2.

## Next Session Entry Point
`docs/09_agents/AgentHandoff.md` (Session Packet, top) → pick T-008/T-009/T-010.
"""


# ============================================================
# writer
# ============================================================

def write_all(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, content in DOCS.items():
        path = out_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append((name, len(content)))
    return written


def print_tree(out_dir: Path):
    print(f"\n{out_dir}/")
    files = sorted(p for p in out_dir.rglob("*") if p.is_file())
    total = 0
    for f in files:
        size = f.stat().st_size
        total += size
        print(f"   {f.relative_to(out_dir).as_posix():50s} {size:>8,} bytes")
    print(f"\n   total: {len(files)} files, {total:,} bytes\n")


def main():
    ap = argparse.ArgumentParser(description="Kepler documentation generator")
    ap.add_argument("--out", default="./docs", help="output folder")
    ap.add_argument("--tree", action="store_true", help="print tree after writing")
    args = ap.parse_args()

    out = Path(args.out)
    print("=" * 70)
    print("Kepler — Documentation Generator")
    print("=" * 70)
    print(f"output: {out.resolve()}")
    print(f"date:   {datetime.now().isoformat()}")
    print(f"files:  {len(DOCS)}")
    print("-" * 70)

    written = write_all(out)
    for name, size in written:
        print(f"  OK {name:50s} {size:>8,} chars")
    if args.tree:
        print_tree(out)
    print("All docs written.")


if __name__ == "__main__":
    main()
