# Concept

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
