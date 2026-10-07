# R-MM-001: Avellaneda–Stoikov → Three-Body Mapping

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
