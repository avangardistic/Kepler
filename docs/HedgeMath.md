# Hedge Mathematics

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
