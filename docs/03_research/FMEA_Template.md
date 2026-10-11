# FMEA Template

## Purpose
Failure Mode and Effects Analysis (FMEA) for systematic risk assessment of new modules.

## When to Use
- Before adding a new physics module
- Before adding a new detector
- Before integrating external data
- After any production bug
- During design review

## FMEA Format

```markdown
## FMEA: [Module Name]

| Failure Mode | Effect | Severity (1-10) | Cause | Occurrence (1-10) | Detection (1-10) | RPN | Action |
|-------------|--------|-----------------|-------|-------------------|------------------|-----|--------|
| [Mode 1] | [Effect] | [1-10] | [Cause] | [1-10] | [1-10] | [S×O×D] | [Action] |
| [Mode 2] | [Effect] | [1-10] | [Cause] | [1-10] | [1-10] | [S×O×D] | [Action] |
```

## Scoring Guide

### Severity (S)
- 1-3: Minor impact, easily tolerated
- 4-6: Moderate impact, workarounds exist
- 7-8: Significant impact, requires attention
- 9-10: Critical impact, system failure

### Occurrence (O)
- 1-3: Rare, < 1% of time
- 4-6: Occasional, 1-10% of time
- 7-8: Frequent, 10-50% of time
- 9-10: Very frequent, > 50% of time

### Detection (D)
- 1-3: Easily detected (tests, logs)
- 4-6: Moderately detectable
- 7-8: Hard to detect
- 9-10: Very hard or impossible to detect

### RPN (Risk Priority Number)
- RPN = Severity × Occurrence × Detection
- Thresholds are defined once, under "Action Thresholds" below.

## Example: FMEA for physics_jax.py

```markdown
## FMEA: physics_jax.py

| Failure Mode | Effect | Severity | Cause | Occurrence | Detection | RPN | Action |
|-------------|--------|----------|-------|------------|-----------|-----|--------|
| Numeric overflow | NaN in L, crash | 9 | 1/d³ blowup | 8 | 2 | 144 | Epsilon softening (implemented) |
| Energy drift | Violated I2 | 7 | Large dt / model-data mismatch | 6 | 3 | 126 | Record as an invariant failure; model decision required (see CON-008). Do not loosen the criterion or introduce a free time step (ADR-006) |
| Zero mass division | NaN in acceleration | 8 | Empty book | 5 | 4 | 160 | Guard with jnp.where (implemented) |
| JAX tracing error | Runtime error | 7 | Python if on traced array | 6 | 5 | 210 | Use jnp.where instead of if (implemented) |
| Pytree registration missing | JIT failure | 8 | Forgot registration | 4 | 3 | 96 | Register on class definition (implemented) |
```

## Action Thresholds

- **RPN > 100:** Must document mitigation in code comments
- **RPN > 200:** Must implement fix before merging
- **RPN > 500:** Cannot proceed — redesign required

## Post-FMEA Checklist
- [ ] All failure modes identified
- [ ] RPN calculated for each
- [ ] Actions documented for RPN > 100
- [ ] Fixes implemented for RPN > 200
- [ ] FMEA recorded in [`ResearchLog.md`](ResearchLog.md)
