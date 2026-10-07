# QA Protocol

## Purpose
This document defines the Quality Assurance workflow for the Three-Body HFT project.

## QA Principles

### P1: Invariant-First
Every code change must preserve all invariants from `Invariants.md`.

### P2: Falsification-First Testing
Tests define rejection criteria. If a test fails, the model (not the test) must be questioned.

### P3: No Threshold Laziness
Test thresholds in `Invariants.md` are fixed. Do not loosen them to make tests pass.

### P4: Reproducibility
All tests must be deterministic and reproducible.

## QA Workflow

### For New Code
1. Write code with type hints and docstrings
2. Write unit tests for all invariants
3. Run tests: `pytest tests/ -v`
4. If all pass: commit with changelog entry
5. If any fail: apply 5 Whys, fix code or reject model

### For Bug Fixes
1. Identify failing invariant
2. Apply 5 Whys to find root cause
3. Fix code (not test threshold)
4. Verify fix with tests
5. Document in ResearchLog.md

### For Refactoring
1. Ensure all tests still pass
2. Verify invariants preserved
3. Update documentation

## Test Categories

### Unit Tests
- Location: `tests/`
- Run with: `pytest tests/ -v`
- Must pass before any commit

### Invariant Tests
- Location: `tests/test_invariants.py` (to be created)
- Test against `Invariants.md`
- Failure = immediate halt

### Integration Tests
- Location: `tests/test_integration.py` (to be created)
- Test cross-module behavior
- Run before major releases

## QA Checklist (per change)
- [ ] All tests pass
- [ ] No invariant violated
- [ ] No threshold loosened
- [ ] Documentation updated
- [ ] ResearchLog updated
- [ ] Changelog updated
- [ ] Decisions updated (if ADR affected)

## CI/CD
When available, automated CI should run:
- `pytest tests/ -v` on every commit
- Block merge if any test fails

## Escalation
If QA cannot be resolved:
1. Document in `Conflicts.md`
2. Notify other agents via `AgentSync.md`
3. Escalate to human if unresolved
