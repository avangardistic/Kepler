# AI and Contributor Protocol

## Purpose

Give a human or AI contributor one practical, auditable workflow. Follow the repository-level instructions in [`../../AGENTS.md`](../../AGENTS.md); this file adds project-specific process, not a second conflicting prompt.

## Source of truth

- **Scope:** [`goal.md`](goal.md), [`../01_theory/Philosophy.md`](../01_theory/Philosophy.md), and [`../01_theory/Axioms.md`](../01_theory/Axioms.md).
- **Implementation:** source code and tests. A document cannot make an unimplemented feature real.
- **Accepted engineering decisions:** [`../02_engineering/Decisions.md`](../02_engineering/Decisions.md).
- **Unresolved contradictions:** [`../03_research/Conflicts.md`](../03_research/Conflicts.md). Do not resolve one by silently editing a threshold or choosing a convenient document.
- **Plans:** [`roadmap.md`](roadmap.md) and [`TaskQueue.md`](TaskQueue.md). They describe intended work, not permission to cross the scope boundaries.
- **History:** the research log and changelog are records, not current specifications.

If code, tests, and prose disagree, inspect the implementation and test evidence, state the mismatch, and update the relevant record. For a scientific or scope decision that is not already accepted, list the options and ask the maintainer rather than guessing.

## Task loop

1. Confirm the requested outcome and inspect `git status` before editing.
2. Read only the relevant project rules, open conflicts, source, and tests; use the documentation index to find them.
3. State a small plan, acceptance criterion, and non-goals. If the task is underspecified, identify the assumption or decision needed.
4. Implement the smallest complete change. Keep speculative modules out of the codebase until they are actually needed.
5. Run the narrowest useful test, then the full suite when feasible. Preserve thresholds. Record the exact command, environment limitations, and result.
6. Review the diff and update only affected documentation. A material experiment/decision belongs in the research log; a notable user-visible change belongs in the changelog.
7. Report outcome, verification, limitations, and follow-up/blocker.

## Coordination

Paperclip or another shared tracker is optional, never assumed. If it is not available, the task queue and [`AgentSync.md`](AgentSync.md) are a lightweight handoff record, not a distributed lock. Do not claim another person's task based only on a stale table. See [`AgentHandoff.md`](AgentHandoff.md).
