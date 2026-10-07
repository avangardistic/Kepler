# Five Whys Template

## Purpose
Root cause analysis protocol for debugging test failures, bugs, or unexpected behavior.

## When to Use
- Test fails unexpectedly
- Bug appears in production code
- Invariant violation detected
- Behavior doesn't match model prediction

## Protocol

Apply 5 Whys iteratively:

```markdown
## 5 Whys Analysis: [Problem Description]

**Problem:** [Clear, specific statement of the observed issue]

**Why 1:** [First answer — direct cause]
**Why 2:** [Deeper cause — why did Why 1 happen?]
**Why 3:** [Deeper cause — why did Why 2 happen?]
**Why 4:** [Deeper cause — why did Why 3 happen?]
**Why 5:** [Root cause — why did Why 4 happen?]

**Root Cause:** [Confirmed technical or systemic cause]
**Fix:** [Action taken to address root cause]
**Verification:** [How you verified the fix works]
```

## Rules

1. **Focus on process, not blame.** The goal is to fix the system, not assign fault.

2. **Branch when needed.** If a single chain doesn't reach root cause, branch into multiple paths:
   ```markdown
   **Branch A:** [path 1]
   **Branch B:** [path 2]
   ```

3. **Document each step.** Write the analysis in `ResearchLog.md` under a dedicated section.

4. **Stop at actionable root cause.** Don't continue past the point where you can take action.

## Example

```markdown
## 5 Whys Analysis: Energy drift in symplectic integrator

**Problem:** Energy drift of 1e-3 observed over 1000 ticks, expected < 1e-6.

**Why 1:** The integrator is not conserving energy to expected precision.
**Why 2:** The time step dt=0.01 is too large for the system dynamics.
**Why 3:** The gravitational forces are large due to close body proximity.
**Why 4:** G_DEFAULT = 1e-6 amplifies forces at small separations.
**Why 5:** G_DEFAULT is a magic constant, not self-derived from system geometry.

**Root Cause:** Use of magic G_DEFAULT constant violates Axiom 4 (self-induced gravity).

**Fix:** Replace G_DEFAULT with G_eff = 1 / <d²>_t (self-derived from system).

**Verification:** Re-run energy conservation test with G_eff. Expected drift < 1e-6.
```

## Template for ResearchLog.md

```markdown
## [YYYY-MM-DD] [5 Whys] [Problem Title]

**Problem:** [description]

**Why 1:** [answer]
**Why 2:** [answer]
**Why 3:** [answer]
**Why 4:** [answer]
**Why 5:** [answer]

**Root Cause:** [cause]
**Fix:** [action]
**Verification:** [method]
```
