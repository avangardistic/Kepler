# R-PHY-001: Virial Theorem for Non-Conservative Systems

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
