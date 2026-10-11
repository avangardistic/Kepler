# Prompt Library

Use one template per task. Replace bracketed fields with real repository facts. Keep the prompt scoped; inspect source and tests rather than treating this text as evidence. The templates follow a simple, Karpathy-inspired loop: define the objective, inspect reality, make the smallest change, run an evaluation, and report honestly.

## P1 — Start or continue a task

```text
Task: [ID or user request]
Outcome: [observable result]
Non-goals: [what must not change]
Acceptance: [tests, measurement, or documentation condition]

Read AGENTS.md and the relevant project docs. Inspect git status, current implementation,
tests, and any relevant open conflict. Do not assume the task queue is current or that
a planned item is implemented. If a scope/model decision is missing, stop and identify
what must be decided. Otherwise make the smallest complete change, run the relevant
checks, inspect the final diff, and report evidence, limitations, and follow-up.
```

## P2 — Implement a behavior or fix

```text
Implement/fix: [behavior or defect]
Reproduction: [test, fixture, or observed behavior]
Acceptance: [specific passing test or measured property]
Constraints: [invariants, interfaces, compatibility]

First inspect the code path and existing tests. Add a test that captures the expected
behavior, make the smallest patch, then run focused and full tests when feasible. Do
not alter thresholds to make the test pass. If the failure reflects a model conflict,
record evidence and ask for a decision instead of coding around it.
```

## P3 — Test a hypothesis

```text
Hypothesis: [one falsifiable claim]
Population/data: [fixture, synthetic setup, or captured dataset]
Metric and rejection criterion: [defined before running]
Confounders / controls: [list]

Check the existing hypothesis and experiment docs for conflicts. Design a reproducible
experiment that can reject the claim. Separate synthetic results from real-data
results. Do not change the criterion after seeing the outcome. Record the command,
environment, raw summary, uncertainty, limitation, and conclusion in the research log.
```

## P4 — Review a conflict or proposed decision

```text
Conflict: [ID]
Question: [decision that is actually needed]
Evidence: [source, tests, fixture, measurements]

Summarize the competing interpretations and their consequences. Verify each against
code and tests. Do not choose a model change on behalf of the maintainer. Recommend
an option only with explicit trade-offs and a re-test plan; otherwise leave the conflict
open and state the decision needed.
```

## P5 — Documentation audit or reorganization

```text
Scope: [files/categories]
Canonical structure: [index or approved plan]

Inventory every source file before moving or rewriting. Preserve historical records,
label proposals versus implemented facts, update links and compatibility paths, and
check for duplicate or stale sources of truth. Afterward verify that every expected
file is present, every internal Markdown link resolves, and the diff contains no
unintended content loss. Do not claim code tests ran for a docs-only change unless
actually run.
```

## P6 — Review a change

```text
Review this diff for correctness, regressions, scope violations, and missing tests.
Prioritize concrete findings by severity and cite file/line. Check that tests match the
claimed behavior, thresholds were not loosened, and evidence is not overstated. Do not
rewrite the implementation; return findings and any unanswered questions first.
```

## P7 — Optimize a measured bottleneck

```text
Bottleneck: [profile result]
Baseline: [command, input size, environment, metric]
Target: [measurable improvement]
Behavior that must remain identical: [contract]

Profile before changing code. Make one isolated optimization, run correctness tests,
and repeat the exact benchmark. Report before/after values and uncertainty. Do not add
a dependency or change outputs without a separate decision.
```

## P8 — Close a session / hand off

```text
Inspect git status and the full diff. State what changed, the exact checks run and
results, what could not be checked, any conflict/decision still open, and the next
useful step. Update task/history records only where the status or evidence changed.
An open conflict is acceptable; an undocumented or mislabelled result is not.
```
