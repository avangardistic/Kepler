# Kepler Documentation Index

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
