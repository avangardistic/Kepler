# Prompt Library

## Standard Prompts

### P1 — Take Next Task
```
Take the next task from TaskQueue.md.
Check current phase and dependencies.
If all prerequisites are met, start.
Report in ResearchLog.md.
```

### P2 — Test Hypothesis
```
Read Hypotheses.md.
Pick one falsifiable hypothesis.
Design the corresponding experiment from Experiments.md.
Write test code in tests/.
Record result in ResearchLog.md.
If rejected, add to FailureModes.md.
```

### P3 — Add New Phase
```
Read roadmap.md.
Take the next phase.
Check prerequisites.
Add a task to TaskQueue.md.
```

### P4 — Check Conflicts
```
Scan all files in docs/.
Log each conflict in Conflicts.md.
Propose resolution.
```

### P5 — Check Invariants
```
Read Invariants.md.
Test each invariant with code.
If failed, write cause in FailureModes.md.
```

### P6 — Optimization
```
Find hot paths (profiling).
If slow, use numba/JAX.
No behavior change, only speed.
```

### P7 — Mathematical Extension
```
Read OpenProblems.md.
Pick one problem.
Give mathematical extension.
If proven, add to Concept.md.
If rejected, record in FailureModes.md.
```

### P8 — Review
```
Read recent changes from Changelog.md.
Are they compatible with Philosophy.md?
If not, log in Conflicts.md.
```
