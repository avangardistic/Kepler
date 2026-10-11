# Handoff Protocol

A useful handoff states what changed, how it was checked, what remains uncertain, and what the next person can do. An unresolved conflict is an acceptable handoff when it is clearly recorded; never mark it resolved merely to make the handoff look complete.

## Before handing off

1. Inspect `git status` and the full diff. Do not overwrite unrelated work.
2. Run relevant tests or state exactly why they could not be run. Include the command and result.
3. Update the task status and the research/changelog only when the underlying status, evidence, decision, or user-visible behavior changed.
4. Record new or changed conflicts in [`../03_research/Conflicts.md`](../03_research/Conflicts.md); leave open questions open.
5. Update [`AgentSync.md`](AgentSync.md) only if it helps another active contributor. Do not invent an active agent or task claim.
6. Do not assume a commit, external post, or clean test run is mandatory if the environment or user has not asked for it.

## Handoff format

```markdown
## Handoff — YYYY-MM-DD
- **Task / scope:**
- **Changed:**
- **Evidence:** command, environment, result (or why not run)
- **Decision made:** ADR / maintainer decision / none
- **Open blocker:** conflict ID and decision needed, or none
- **Next useful step:**
```

## Starting a task

Read [`MISSION_PROMPT.md`](MISSION_PROMPT.md), check the current tree and open conflicts, then choose work that is both in scope and unblocked. The task queue is a backlog; it is not proof that prerequisites are satisfied.
