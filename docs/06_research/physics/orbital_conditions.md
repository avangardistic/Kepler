# R-PHY-003: Orbital Stability & Resolution Conditions

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
