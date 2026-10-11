# Kepler Mission Prompt

> **Mission for incoming agent / contributor, generated 2026-10-11**
>
> You are working on **Kepler**, a mathematical research project that tests whether three-body gravitational dynamics provide a valid descriptive language for high-frequency market microstructure using only raw L2 order-book tick data.
>
> This is **not a trading system**. There is no execution, no capital at stake, no profit claims, no price prediction, and no sellable strategy. If you find yourself building any of those, stop and re-read `docs/Philosophy.md`.

---

## 1. Project Identity

| Aspect | Fact |
|--------|------|
| **Core idea** | Treat three assets (BTC, ETH, SOL) as three gravitational bodies in log-microprice space, with all parameters derived internally from the geometry of the L2 order book. |
| **Time unit** | One tick (no seconds, no candles). |
| **Only allowed input** | Raw L2 tick data (bids/asks, prices and quantities). No external parameters, no filters, no indicators, no risk management. |
| **Goal** | Demonstrate that this framing works as a descriptive language, verified by four hard success criteria. |
| **Anti-goals** | Trading bot, signal generator, price prediction model, sellable strategy. |

---

## 2. Immutable Constraints (Never Violate)

1. **Only raw L2 tick data** as input. No derived data, no external data feeds.
2. **No magic constants / free parameters.** All physical quantities (mass, coupling G, friction, force) must be derived from geometry of the book.
3. **No filters, no indicators.** The orbit is the filter; gravity is the indicator.
4. **No risk management.** Risk is assumed to be solved by orbital geometry. If you feel you need a stop-loss, the model is wrong.
5. **No execution.** This project never trades, never connects to an exchange for order placement, never claims profit.
6. **Preserve all invariants** in `docs/Invariants.md`. Test thresholds are fixed — never loosen a threshold to make a test pass.
7. **Time quantized in ticks.**
8. **Documentation first, code second** (per `docs/AI_Protocol.md`). Update docs before or alongside code changes.

---

## 3. Success Criteria (The Project Fails If These Are Not Met)

1. **Angular momentum ‖L‖ remains bounded** — relative error < 1e-9 for conservative subsystem.
2. **Virial ratio ⟨T⟩/⟨V⟩ → −1/2** for conservative subsystem; generalized form holds when friction/imbalance are present. Tolerance: |⟨T⟩/⟨V⟩ + 0.5| < 0.2 after equilibration.
3. **Π > 0 in mathematical expectation** (profit = work, ∮ p·dx).
4. **Zero max drawdown** via self-freeze on empty/jumpy books.

---

## 4. Current Repository State (Audited 2026-10-11)

### What exists and works:
- `src/physics_jax.py` — complete three-body physics engine in JAX (float64):
  - Velocity-Verlet symplectic integrator (`symplectic_step`, `integrate` via `lax.scan`).
  - `ThreeBodyState` pytree with positions, velocities, masses, imbalance, friction.
  - Energy, angular momentum, virial ratio, self-induced G calculations.
  - `state_from_l2` to build a state from three raw L2 books.
  - Rigid-rotation embedding for 1D states (ADR-008, no magic constants).
  - Zero-mass (empty book) handling without NaN (self-freeze behavior).
- **All 9 tests pass**: `PYTHONPATH=. pytest tests/ -v` → 9 passed (JAX 0.10.2, pytest 9.1.1, Python 3.11).
- Full documentation set in `docs/`: philosophy, axioms, invariants, physics, roadmap, task queue, research log, conflicts, ADRs, QA protocol.

### What does NOT exist yet (despite old changelog entries, these were planned milestones, not delivered code):
- ❌ `fast_l2_client` (Phase 1 WebSocket ingestion)
- ❌ `tick_buffer` / Parquet storage / replay tool
- ❌ `detectors_numba` (regime detection)
- ❌ `market_maker` (market-making logic)
- ❌ `simulation_live_v3` / 10M-tick simulation
- ❌ Validation experiments / hypothesis testing

### Roadmap progress:
- **Phase 0 (Theoretical Foundation):** ✅ Complete
- **Phase 2 (Physics engine):** ✅ Complete (invariants hold, tests pass)
- **Phase 1 (Tick Infrastructure):** ⬜ Not started — **highest priority, blocks all later phases**
- **Phase 3 (Detectors):** ⬜ Blocked by Phase 1
- **Phase 4 (Market Making):** ⬜ Blocked by Phase 1
- **Phase 5–10:** ⬜ Blocked by earlier phases

### Open known gaps (documented, do not hide them):
1. **CON-005 remark:** `integrate` currently uses G computed from the initial state (held fixed); `docs/Physics.md` specifies a running time-average of ⟨d²⟩_t. Decision needed before Phase 5.
2. **N ≥ 3 rigid-rotation residual:** The ADR-008 rigid embedding is exact for two bodies; residual error for true three-body configurations has not been measured yet.

---

## 5. Your Immediate Mission

The highest-priority unblocking work is **Phase 1: Tick Infrastructure**. Without recorded L2 tick data, every later phase (detectors, market making, simulation, validation) cannot run on real data.

The next tasks are **T-001 (fast_l2_client)** and **T-002 (tick_buffer + Parquet storage + replay)**, per `docs/TaskQueue.md`.

### T-001 — fast_l2_client
Design and implement a fast L2 tick client (following ADR-004: `uvloop` + `orjson` where applicable) that:
- Connects to a public L2 WebSocket feed (BTC, ETH, SOL, or three correlated assets).
- Streams raw L2 order-book updates (bids/asks at all levels, no aggregation).
- Delivers ticks in order, no drops (exit criterion: 100,000 ticks without drop).
- Does no processing, no filtering, no indicator calculation. Only raw data.
- Adheres to all axioms: no external parameters, no magic configuration beyond what is required to connect.

### T-002 — tick_buffer + Parquet storage + replay
Implement a tick buffer and storage layer that:
- Writes raw L2 ticks to Parquet, preserving all fields (timestamp in ticks, bid levels, ask levels, quantities).
- Provides a deterministic replay utility that can feed stored ticks back into `state_from_l2` and the `integrate` loop.
- Guarantees tick ordering and no data corruption.
- Works offline so physics / detector / simulation tests can run without an open WebSocket.

These two tasks unblock every other open task (T-005 through T-007). If you cannot complete both in one session, finish what you can, document progress in `docs/ResearchLog.md`, update `docs/AgentSync.md`, and hand off cleanly per `docs/AgentHandoff.md`.

---

## 6. Operating Rules (Follow These On Every Change)

1. **Read first, code second.** Follow the start-up sequence from `README.md`:
   1. `docs/goal.md`, `docs/Philosophy.md`, `docs/Axioms.md`, `docs/Invariants.md`
   2. Last 5 entries of `docs/ResearchLog.md`
   3. `docs/Conflicts.md`, `docs/Decisions.md`
   4. `docs/roadmap.md`, `docs/TaskQueue.md`
   5. Claim your task in `docs/AgentSync.md` before starting.
2. **Invariant-first.** Every code change must preserve I1–I7. Run `PYTHONPATH=. pytest tests/ -v` before every commit. All 9 existing tests must still pass.
3. **No threshold loosening.** If a test fails, fix the model or the code, not the test criterion (QA Protocol P3).
4. **Document as you go:**
   - State changes → `docs/ResearchLog.md`
   - Conflicts / inconsistencies → `docs/Conflicts.md`
   - Architecture decisions → new ADR entry in `docs/Decisions.md`
   - User-visible changes → `docs/Changelog.md`
5. **No magic constants.** If you find yourself hardcoding a number, stop. Derive it from geometry or log a high-severity conflict.
6. **Keep tests deterministic** (QA Protocol P4). No randomness in tests without a fixed seed.
7. **Follow ADR-009:** Python + JAX for physics; numba reserved for detectors. Do not introduce new languages (C/Rust/C++) unless measured performance proves it necessary and an ADR is recorded.
8. **When stopping** — follow `docs/AgentHandoff.md`: update AgentSync, ensure tests pass, update ResearchLog and Changelog, leave no unresolved conflict open.

---

## 7. Verification

The baseline verification command (must always pass from repo root):
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -v
```
Expected result: **9 passed**.

Any new code you add must include unit tests in `tests/` covering relevant invariants, and must be added to `requirements.txt` if it introduces new dependencies (keep dependencies minimal and justified).

---

## 8. Falsifiability

The project is falsifiable. It fails (and you must document the failure) if:
1. There is a sudden price gap without corresponding volume.
2. The L2 book goes to zero depth (jump-to-zero) without triggering self-freeze.
3. An external disruption (major news, exchange outage) invalidates the closed-system assumption.
4. Any invariant is violated on real tick data and cannot be fixed by correcting the model (without loosening thresholds).

When you falsify a hypothesis, add the failure mode to `docs/FailureModes.md` and log it in the ResearchLog — falsification is progress, not a setback.

---

## 9. Conflict Resolution Order

If you encounter a contradiction between documents or between code and docs:
1. `docs/Philosophy.md` wins over everything else.
2. `docs/Axioms.md` wins over all other technical docs.
3. `docs/AI_Protocol.md` wins over process docs.
4. If none of the above resolve it, log the conflict in `docs/Conflicts.md` and escalate to human. Do not guess.

---

**Start here:** Read `docs/TaskQueue.md` to confirm T-001 and T-002 are still open and unclaimed, claim the next task in `docs/AgentSync.md`, then begin design and implementation following the rules above.
