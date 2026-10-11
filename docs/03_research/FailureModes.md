# Failure Modes

> The "Response" lines describe expected or intended model behavior — hypotheses,
> not verified guarantees. Only F10 is an observed result. Detector-related
> entries refer to the unimplemented draft in [`../02_engineering/Detectors.md`](../02_engineering/Detectors.md).

## F1 — Jump-to-Zero Depth
**Scenario:** Order book depth drops to zero in a single tick.
**Expected response:** $m \to 0$ and the body freezes. The physics path keeps such states finite (synthetic test), but the broader self-freeze criterion is not established; see [`goal.md`](../04_planning/goal.md), [H4](Hypotheses.md), and [E3](Experiments.md).
**Severity:** Low (self-correcting in the tested zero-depth cases).

## F2 — Cross-Exchange Divergence
**Scenario:** Binance and Coinbase diverge by 5%.
**Status:** outside the current input scope — the pipeline ingests a single venue's snapshots (Assumptions.md §5), so no cross-exchange response is implemented or modeled.
**Severity:** Medium (short-term) if the scope is ever extended.

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
**Mitigation (Phase 1, 2026-10-11):** `src/fast_l2_client.py` uses pull semantics (a lagging consumer pauses the reader) plus a blocking producer queue, so no tick can be dropped by the client (`TickStats.dropped` stays 0, asserted over 100 000 ticks); `src/tick_buffer.py` rejects a decreasing `tick_index` with `TickOrderError` instead of silently reordering (`out_of_order` is counted live). A storage-level loss can still occur only if the process dies between flushes — the unflushed block is the exposure window.
**Severity:** Medium.

## F7 — Symplectic Drift
**Scenario:** Cumulative numeric error.
**Implemented response:** velocity-Verlet (symplectic) integration with O(Δt²) energy behavior; the constraint-manifold projection in [`Symplectic.md`](../01_theory/Symplectic.md) §4 is a proposal and is not implemented.
**Severity:** Low in the synthetic conservative tests; on real replay the drift is observed and is tracked in F10/CON-008.

## F8 — Virial Breakdown
**Scenario:** $T/V$ diverges from $-1/2$.
**Expected response:** in the conservative subsystem the synthetic test converges to the I4 criterion; real-data behavior is not established.
**Severity:** Monitored — a divergence is a falsification signal, not a self-healing guarantee.

## F9 — Generalized Virial Test Failure
**Scenario:** Generalized virial theorem $|2\langle T \rangle + \langle V \rangle + \langle F_{ext} \cdot x \rangle + \langle F_{friction} \cdot x \rangle| > \text{threshold}$.
**Response:** Log as falsification in FailureModes.md. Do NOT loosen threshold.
**Severity:** Varies — may indicate model inadequacy.
**Status:** MONITORED

## F10 — Invariants fail on real L2 data at dt = 1 tick (OBSERVED 2026-10-11)
**Scenario:** Live L2 ticks (BTC/ETH/SOL, Binance `depth20@100ms`, 2 785 ticks
captured 2026-10-11) replayed through `state_from_l2` and integrated with
`dt = 1` tick (ADR-006).
**Observation (measured, not inferred):**

| Path (2 000 ticks, dt = 1) | ‖L‖₀ | ‖L‖ₘₐₓ | E₀ | max relative energy drift |
|---|---|---|---|---|
| 2-D state as returned by `state_from_l2`, conservative | 0 | 0 | −1.008 | **281** |
| 2-D state, with imbalance and friction | 0 | 6.25e4 | −1.008 | **6.2e6** |
| 1-D state ⇒ ADR-008 rigid-rotation embedding, conservative | 8.484 | 8.484 | −0.6255 | **1.54** |
| 1-D state ⇒ ADR-008 embedding, with imbalance and friction | 8.484 | 1.65e6 | −0.6255 | **1e7** |

* I2 (relative drift < 1e-9) fails by 9–15 orders of magnitude in every path.
* I1 holds only in the conservative case without imbalance: the gravitational
  force is central for co-linear bodies, so L stays 0 (2-D path) or constant
  (1-D embedded path). Non-zero imbalance excites L, because the scalar
  imbalance is applied to **every** component of the acceleration
  (`a_i = grav + I_i − γ_i v_i / m_i`, with `I_i` a scalar per body).
* `state_from_l2` returns a **2-D** state (`x` has shape (3, 2), transverse
  velocity 0), so `_stabilized_state` never applies ADR-008's rigid-rotation
  embedding to L2-built states. The embedding is only reached for 1-D input.
  Applying it manually bounds L for the conservative case but does **not**
  restore I2 — consistent with ADR-008's own caveat that rigid rotation is
  exact for two bodies only. The N ≥ 3 residual, previously unmeasured, is now
  measured on real data: it does not preserve energy at dt = 1.
* No threshold was loosened: `tests/` is unchanged in its criteria and still
  passes 41/41, because those tests use purpose-built 2-body / symmetric
  configurations, not live books.

**Response:** Logged as CON-008 in Conflicts.md (open, escalated to human) with
three candidate directions (time-scale calibration, applying the embedding to
L2 states, and the CON-005 running-average G). NOT fixed here: every candidate
changes the model and needs an ADR, per the conflict-resolution order.
**Severity:** High — it blocks Phase 5 (Π > 0 on 10 M ticks) until resolved.
**Status:** OPEN
