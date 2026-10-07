# R-PHY-004: Generalized Virial Theorem (driven + damped Kepler)

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
