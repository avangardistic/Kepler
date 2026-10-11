# Kepler Documentation Map

> **Canonical navigation hub.** The 48 topic documents are organized into five numbered categories. Edit the canonical file in its category; flat files such as `docs/Axioms.md` are compatibility stubs only.

**Reviewed:** 2026-10-11 · **Current gate:** CON-008 remains open · **Last recorded suite:** 41 passed in the pinned environment (not re-run by this documentation migration).

## Start here

| Need | Read |
|---|---|
| What the project is and is not | [`04_planning/goal.md`](04_planning/goal.md) |
| What is implemented and what is blocked | [`04_planning/roadmap.md`](04_planning/roadmap.md) and [`04_planning/TaskQueue.md`](04_planning/TaskQueue.md) |
| Agent/contributor workflow | [`AGENTS.md`](../AGENTS.md), then [`04_planning/MISSION_PROMPT.md`](04_planning/MISSION_PROMPT.md) |
| Current scientific blockers | [`03_research/Conflicts.md`](03_research/Conflicts.md), especially CON-008/CON-009 |
| Install, test, capture, and replay | [`../README.md`](../README.md) |

## 01 · Theory

Foundations, model definitions, and mathematical claims. Claims remain hypotheses until their criteria are met.

| Document | Role |
|---|---|
| [`01_theory/Assumptions.md`](01_theory/Assumptions.md) | Data/model assumptions and validity boundaries |
| [`01_theory/Axioms.md`](01_theory/Axioms.md) | Project constraints, model definitions, and provisional claims |
| [`01_theory/Concept.md`](01_theory/Concept.md) | Model vocabulary and state construction |
| [`01_theory/Differential.md`](01_theory/Differential.md) | Differential-geometry extension notes |
| [`01_theory/GaugeTheory.md`](01_theory/GaugeTheory.md) | Gauge-theory analogy/proposal |
| [`01_theory/Geometry.md`](01_theory/Geometry.md) | Orbital geometry notes |
| [`01_theory/HedgeMath.md`](01_theory/HedgeMath.md) | Proposed hedge arithmetic; not an execution layer |
| [`01_theory/Invariants.md`](01_theory/Invariants.md) | I1–I7 and Phase 1 retention criteria |
| [`01_theory/Microprice.md`](01_theory/Microprice.md) | Microprice definition |
| [`01_theory/OrderBookMath.md`](01_theory/OrderBookMath.md) | L2 order-book arithmetic |
| [`01_theory/Philosophy.md`](01_theory/Philosophy.md) | Research scope and epistemic boundaries |
| [`01_theory/Physics.md`](01_theory/Physics.md) | Lagrangian, forces, energy, virial relation, coupling |
| [`01_theory/Quantum.md`](01_theory/Quantum.md) | Quantum analogy notes; speculative |
| [`01_theory/Strategy.md`](01_theory/Strategy.md) | Historical, unvalidated non-executable strategy sketch; T-006 blocked |
| [`01_theory/Symplectic.md`](01_theory/Symplectic.md) | Symplectic integration notes |
| [`01_theory/TickModel.md`](01_theory/TickModel.md) | Tick-time definition |

## 02 · Engineering

Implementation contracts, decisions, and quality gates. A specification does not mean the module exists.

| Document | Role |
|---|---|
| [`02_engineering/DataSpec.md`](02_engineering/DataSpec.md) | Raw L2 schema, storage, and validation |
| [`02_engineering/Decisions.md`](02_engineering/Decisions.md) | Architecture decision records (ADR-001–ADR-011) |
| [`02_engineering/Detectors.md`](02_engineering/Detectors.md) | Detector specification; implementation is not present |
| [`02_engineering/Implementation.md`](02_engineering/Implementation.md) | Implemented architecture versus planned pipeline |
| [`02_engineering/MarketMaking.md`](02_engineering/MarketMaking.md) | Unimplemented proposal, blocked by scope conflict CON-009 |
| [`02_engineering/QA_Protocol.md`](02_engineering/QA_Protocol.md) | Test and evidence workflow |
| [`02_engineering/ToolSelection.md`](02_engineering/ToolSelection.md) | Recorded language/tool selection analysis |

## 03 · Research

Evidence, uncertainty, failure analysis, and research history.

| Document | Role |
|---|---|
| [`03_research/Changelog.md`](03_research/Changelog.md) | User-visible and project changes; planned releases are marked as such |
| [`03_research/Conflicts.md`](03_research/Conflicts.md) | Resolved and open contradictions; CON-008/CON-009 remain open |
| [`03_research/Experiments.md`](03_research/Experiments.md) | Proposed experiment catalogue; not a record of completed tests |
| [`03_research/FailureModes.md`](03_research/FailureModes.md) | Known failure modes, including F10 real-data failure |
| [`03_research/Falsifiability.md`](03_research/Falsifiability.md) | Rejection criteria and current evidence status |
| [`03_research/FMEA_Template.md`](03_research/FMEA_Template.md) | Failure-mode analysis template |
| [`03_research/Five_Whys_Template.md`](03_research/Five_Whys_Template.md) | Root-cause analysis template |
| [`03_research/Hypotheses.md`](03_research/Hypotheses.md) | Provisional, testable claims and status |
| [`03_research/Limitations.md`](03_research/Limitations.md) | Known limitations and scope boundaries |
| [`03_research/OpenProblems.md`](03_research/OpenProblems.md) | Open mathematical questions |
| [`03_research/PriorArt.md`](03_research/PriorArt.md) | Prior-art notes |
| [`03_research/RegimeCatalog.md`](03_research/RegimeCatalog.md) | Proposed L2 regime catalog |
| [`03_research/ResearchLog.md`](03_research/ResearchLog.md) | Dated evidence and session history |

## 04 · Planning and workflow

Mission, work queue, coordination, and contributor prompts.

| Document | Role |
|---|---|
| [`04_planning/AI_Protocol.md`](04_planning/AI_Protocol.md) | Source-of-truth and task loop |
| [`04_planning/AgentHandoff.md`](04_planning/AgentHandoff.md) | Clean handoff format |
| [`04_planning/AgentSync.md`](04_planning/AgentSync.md) | Optional lightweight manual claims and blockers |
| [`04_planning/MISSION_PROMPT.md`](04_planning/MISSION_PROMPT.md) | Current onboarding prompt |
| [`04_planning/Paperclip_Coordination.md`](04_planning/Paperclip_Coordination.md) | Optional external coordination guidance |
| [`04_planning/PromptLibrary.md`](04_planning/PromptLibrary.md) | Scoped prompts for implementation, research, review, and handoff |
| [`04_planning/TaskQueue.md`](04_planning/TaskQueue.md) | Current task status, dependencies, and gates |
| [`04_planning/goal.md`](04_planning/goal.md) | Project objective, boundaries, and claim status |
| [`04_planning/roadmap.md`](04_planning/roadmap.md) | Phases and evidence gates |

## 05 · Reference

| Document | Role |
|---|---|
| [`05_reference/Glossary.md`](05_reference/Glossary.md) | Domain terms |
| [`05_reference/Notation.md`](05_reference/Notation.md) | Symbols and notation |
| [`05_reference/References.md`](05_reference/References.md) | Bibliography |

## Suggested reading paths

- **New contributor:** `AGENTS.md` → goal → Axioms + Invariants → open Conflicts → relevant source/tests → QA Protocol.
- **Physics/research:** Axioms → Concept → Physics → Invariants → CON-008/F10 → ResearchLog.
- **Data/engineering:** DataSpec → Decisions ADR-010/011 → Implementation → client/buffer source and tests.
- **Reviewer:** goal → Conflicts + FailureModes → changed code/tests → QA checklist.

## Organization and compatibility

Canonical documents live in `01_theory/`, `02_engineering/`, `03_research/`, `04_planning/`, and `05_reference/`. The root-level markdown files for moved documents are small compatibility stubs that link to their canonical locations; do not edit the stubs. `INDEX.md` and `prompt.md` are also compatibility entry points.

Internal links in maintained docs should target canonical paths. Preserve a compatibility stub when moving a file so older repository links continue to resolve. `README.md` at the repository root is the user-facing project overview; [`../CONTRIBUTING.md`](../CONTRIBUTING.md) and [`../CHANGES_TEMPLATE.md`](../CHANGES_TEMPLATE.md) describe contributor reporting.
