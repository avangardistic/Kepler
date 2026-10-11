# Kepler Documentation Index

> **Navigation hub for all 48 project documents.**  
> Start here to find the right doc for your task. Every link is relative to `docs/`; the project root is `../`.

**Last updated:** 2026-10-11 · **Status:** `stable` · **Validated:** `Python 3.11 / jax 0.10.2 / pytest 9.1.1 (41 tests)`

---

## Quick Start

| You want to… | Read… |
|---|---|
| Understand what Kepler is / is not | [`goal.md`](goal.md) — goals, constraints, anti-goals |
| Clone, install, run tests or capture ticks | [`../README.md`](../README.md#getting-started) |
| See the big picture in one page | [`Concept.md`](Concept.md) |

---

## 1 · Conceptual Foundation — *what the model claims*

| Document | Description |
|---|---|
| [`Concept.md`](Concept.md) | Core model definitions: microprice, mass, imbalance, friction |
| [`Axioms.md`](Axioms.md) | 6 axioms the implementation must respect (no external params, tick time, …) |
| [`Invariants.md`](Invariants.md) | Physical & retention invariants I1–I7 + test criteria |
| [`Physics.md`](Physics.md) | Lagrangian, Euler-Lagrange, virial theorem, self-induced gravity |
| [`Symplectic.md`](Symplectic.md) | Why the velocity-Verlet integrator conserves E and L |
| [`Geometry.md`](Geometry.md) | Orbital-plane geometry notes |
| [`Microprice.md`](Microprice.md) | Microprice derivation |
| [`OrderBookMath.md`](OrderBookMath.md) | Order-book arithmetic |
| [`TickModel.md`](TickModel.md) | Tick as time quantum |
| [`Differential.md`](Differential.md) | Differential-form notes |
| [`GaugeTheory.md`](GaugeTheory.md) | Gauge-theory sketch |
| [`Quantum.md`](Quantum.md) | Quantum analogy sketch |
| [`Notation.md`](Notation.md) | Symbol table |

**Cross-links:** `Concept → Axioms → Invariants → Physics → Symplectic`. For the self-induced coupling `G_eff = 1/⟨d²⟩` see Axiom 4 and `Physics §Self-Induced Gravity`.

---

## 2 · Engineering & Decisions — *how it is built*

| Document | Description |
|---|---|
| [`Decisions.md`](Decisions.md) | 11 ADRs (microprice, JAX, uvloop/orjson where-applicable, embedding, …) |
| [`Implementation.md`](Implementation.md) | Architecture, stack, folder layout, tick flow (implemented vs planned) |
| [`ToolSelection.md`](ToolSelection.md) | Why Python + JAX was kept (measured 3.3 M ticks/s) |
| [`DataSpec.md`](DataSpec.md) | L2 schema, Parquet/zstd layout, validation semantics, codec check |
| [`QA_Protocol.md`](QA_Protocol.md) | Invariant-first, falsification-first QA workflow |
| [`AI_Protocol.md`](AI_Protocol.md) | Agent protocol |
| [`AgentSync.md`](AgentSync.md) | Multi-agent sync log |
| [`AgentHandoff.md`](AgentHandoff.md) | Handoff notes |
| [`Assumptions.md`](Assumptions.md) | Explicit assumptions |
| [`Strategy.md`](Strategy.md) | Strategy sketch |
| [`HedgeMath.md`](HedgeMath.md) | Hedge arithmetic |
| [`Limitations.md`](Limitations.md) | Known scoping limits |

**Storage layout (DataSpec §Storage):** `<root>/symbol=<S>/day=<YYYY-MM-DD>/part-NNNN.parquet`, Parquet + zstd, one row per tick. Columns are frozen (`TICK_SCHEMA` in `src/tick_buffer.py`).

---

## 3 · Quality & Validation — *how we know it is wrong or right*

| Document | Description |
|---|---|
| [`Conflicts.md`](Conflicts.md) | 8 conflicts (CON-001…CON-008); CON-008 is **open, escalated** |
| [`FailureModes.md`](FailureModes.md) | 10 failure modes; F10 = real-data invariant failure (measured table) |
| [`Falsifiability.md`](Falsifiability.md) | Falsification criteria |
| [`FMEA_Template.md`](FMEA_Template.md) | FMEA template |
| [`Five_Whys_Template.md`](Five_Whys_Template.md) | 5-Whys template |
| [`Hypotheses.md`](Hypotheses.md) | Hypotheses log |
| [`Experiments.md`](Experiments.md) | Experiments log |
| [`PriorArt.md`](PriorArt.md) | Prior art survey |
| [`RegimeCatalog.md`](RegimeCatalog.md) | Market-regime catalog |
| [`Detectors.md`](Detectors.md) | Detector spec (Phase 3, not yet implemented) |
| [`MarketMaking.md`](MarketMaking.md) | Market-making spec (Phase 4) |
| [`OpenProblems.md`](OpenProblems.md) | Open research questions |

**Key falsification (2026-10-11):** replaying 2 785 live ticks at `dt = 1` fails I2 by 9–15 orders of magnitude in every path. See `FailureModes F10` and `Conflicts CON-008`. No threshold has been loosened.

---

## 4 · Planning & Progress — *where we are going*

| Document | Description |
|---|---|
| [`roadmap.md`](roadmap.md) | Phases 0–5 |
| [`TaskQueue.md`](TaskQueue.md) | T-000…T-007 (T-001/T-002 done, T-005 next, CON-008 blocks T-007) |
| [`MISSION_PROMPT.md`](MISSION_PROMPT.md) | Canonical onboarding prompt for a fresh agent |
| [`prompt.md`](prompt.md) | Alias of the mission prompt |
| [`Philosophy.md`](Philosophy.md) | Project philosophy |
| [`Changelog.md`](Changelog.md) | Version history + 2026-10-07/10/11 migration notes |
| [`ResearchLog.md`](ResearchLog.md) | Dated session log (most detailed history) |
| [`Paperclip_Coordination.md`](Paperclip_Coordination.md) | Coordination notes |
| [`PromptLibrary.md`](PromptLibrary.md) | Prompt library |

**Current status (README):** Phase 0 done · Phase 1 done (41 tests) · Phase 2 implemented (CON-008 open) · Phase 3+ not started.

---

## 5 · Reference — *lookup*

| Document | Description |
|---|---|
| [`Glossary.md`](Glossary.md) | Domain glossary |
| [`Notation.md`](Notation.md) | Symbols & units |
| [`References.md`](References.md) | Bibliography |

---

## Suggested Reading Order

**New contributor (30 min):**
1. [`goal.md`](goal.md) → 2. [`Concept.md`](Concept.md) → 3. [`Axioms.md`](Axioms.md) + [`Invariants.md`](Invariants.md) →
4. [`Physics.md`](Physics.md) §1–3 → 5. [`../README.md`](../README.md#getting-started) → 6. `pytest tests/ -v`

**Physicist:** Axioms → Physics → Symplectic → Decisions ADR-008 → Conflicts CON-008 → FailureModes F10

**Engineer:** DataSpec → Implementation → Decisions ADR-010/011 → `src/fast_l2_client.py` → `src/tick_buffer.py` → `src/physics_jax.py`

**QA / Reviewer:** Invariants → QA_Protocol → Conflicts + FailureModes → ResearchLog (2026-10-11)

---

## Document Organisation — Current vs Planned

**Current:** all 48 files are flat in `docs/` (intentional — avoids churn while Phases 0–2 are stabilising).

**Planned (audit §2.2, not yet executed):**

```
docs/
├── 01_theory/         Axioms, Concept, Physics, Invariants, Symplectic, …
├── 02_engineering/    Decisions, Implementation, ToolSelection, DataSpec, QA_Protocol, …
├── 03_research/       Conflicts, FailureModes, Hypotheses, ResearchLog, Changelog, …
├── 04_planning/       roadmap, TaskQueue, MISSION_PROMPT, OpenProblems, …
├── 05_reference/      Glossary, Notation, References
└── README.md          ← you are here
```

A reorganisation will be a **pure move** (no content edits) with a redirect shim (`docs/<old>.md → docs/<new>/…`) and a single PR that updates every internal link. It is deferred until CON-008 is resolved to avoid mixing model changes with doc moves.

---

## Conventions

- **Time** is quantised in ticks (`TickModel.md`, `Decisions ADR-006`): one tick = one L2 `depth20@100ms` update.
- **Inputs:** only raw L2 ticks (Axiom 1). No derived quantities are stored; physics quantities are recomputed at replay.
- **G** is self-induced `G_eff = 1/⟨d²⟩` (Axiom 4), not a constant (ADR-007 rejected).
- **Thresholds** in `Invariants.md` are fixed — tests never loosen them (`QA_Protocol P3`).
- **Every doc link** in `README.md` and `docs/` uses the flat path `docs/<name>.md` until a reorg lands.

---

## Related

- [`../README.md`](../README.md) — project overview, requirements, tick-capture & replay examples
- [`../CHANGES_TEMPLATE.md`](../CHANGES_TEMPLATE.md) — standard change-report format (policy-alignment checklist)
- [`Invariants.md`](Invariants.md) — invariant table with test names & criteria (single source of truth)
