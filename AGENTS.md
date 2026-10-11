# Kepler — Agent Instructions

This is the short, repo-wide operating prompt. Keep it factual and small; task-specific detail belongs in the linked docs.

## Mission and boundaries

Kepler is a research codebase testing whether a three-body model can describe selected L2 order-book behavior. It is **not** a trading system, signal generator, price predictor, or financial-risk solution. Do not add order placement, live execution, investment advice, or claims of real-world profitability.

Use raw L2 snapshots as the modeled input. Do not quietly add indicators, filters, external features, or fitted constants. Treat model assumptions as hypotheses, not facts. See [`docs/04_planning/goal.md`](docs/04_planning/goal.md), [`docs/01_theory/Axioms.md`](docs/01_theory/Axioms.md), and [`docs/01_theory/Invariants.md`](docs/01_theory/Invariants.md).

## Working loop

Use a small, evidence-led loop (Karpathy-inspired; this is a practical convention, not a formal standard):

1. **Orient:** inspect `git status`, the requested task, relevant source/tests, the roadmap/task queue, and any open conflict that affects the work.
2. **Define:** write down the intended behavior, non-goals, and a testable acceptance criterion. If a model or scope decision is missing, surface it instead of guessing.
3. **Change:** make the smallest coherent patch. Prefer existing dependencies and architecture; do not create scaffolding for hypothetical future modules.
4. **Verify:** run focused tests, then the full suite when feasible. Report commands and actual results. Never loosen an invariant or threshold merely to pass.
5. **Review:** inspect the complete diff for accidental changes, stale claims, and broken links. Update only the docs whose facts or decisions changed.
6. **Report:** summarize what changed, evidence, limitations, and unresolved decisions.

## Evidence and documentation

- Implementation behavior is established by the source and tests; prose is not proof.
- The goal and axioms define project scope. Accepted ADRs record engineering decisions. `Conflicts.md` records unresolved contradictions. The roadmap and task queue are plans, not authority to bypass those boundaries.
- Do not present a planned item as implemented, a synthetic test as real-data validation, or an unrun test as passing.
- Record material experiments and model decisions in the research log; use the changelog for notable user-visible changes. Routine typo fixes do not need a research entry.
- A conflict may remain open at handoff. Record its evidence and blocker; do not invent a resolution.
- Multi-agent services are optional. Do not claim or alter a task in an external tracker unless that integration is actually available and authorized.

## Verification

From the repository root, install the pinned dependencies with `python -m pip install -r requirements.txt`, then run `python -m pytest -q`. If dependencies or network access are unavailable, say so and use non-invasive checks such as `git diff --check` and a documentation-link audit; do not claim the test suite passed.

For onboarding and reusable task prompts, see [`docs/04_planning/MISSION_PROMPT.md`](docs/04_planning/MISSION_PROMPT.md) and [`docs/04_planning/PromptLibrary.md`](docs/04_planning/PromptLibrary.md). The documentation map is [`docs/README.md`](docs/README.md).
