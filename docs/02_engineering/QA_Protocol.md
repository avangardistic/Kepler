# Quality and Verification Protocol

## Principles

1. **Falsify before promoting:** tests and experiments must be capable of rejecting the claim they purport to support.
2. **Keep criteria fixed:** do not loosen an invariant or test threshold to make a failing implementation pass. A proposed change to a scientific criterion requires an explicit decision, rationale, and recorded evidence.
3. **Separate evidence classes:** synthetic/unit tests, offline replay, and live-feed measurements are different. Label each one; never generalize one into another.
4. **Reproduce:** use deterministic fixtures and injected clocks/transports where practical. Keep data provenance with any committed fixture.
5. **Report honestly:** an unrun test is not a pass. A known failure is part of the result.

## Change workflow

### New behavior

1. Identify the behavior, constraints, and acceptance criterion before implementation.
2. Add or update a test that would fail if the behavior were wrong.
3. Implement the smallest change that meets the criterion.
4. Run focused tests, then `python -m pytest -q` when the required dependencies are available.
5. Inspect the diff and update the relevant spec/status docs.

### Bug or model mismatch

1. Reproduce the failure with the smallest available example or fixture.
2. Separate a code defect from a model/assumption conflict.
3. Do not tune thresholds to hide the failure. If the scientific model or scope must change, document options and request the decision.
4. Record material evidence in `../03_research/ResearchLog.md`; update `../03_research/Conflicts.md` when unresolved.

### Documentation-only change

Check every link, distinguish current facts from proposals/history, and avoid claiming that tests ran if the change did not run them.

## Existing test layout

- `tests/test_physics.py` — physics implementation tests.
- `tests/test_fast_l2_client.py` — raw client and retention behavior.
- `tests/test_tick_buffer.py` — storage and replay.
- `tests/data/live_2026-10-11/` — captured data fixture; its presence does not prove the physics invariants pass on real data.

The latest repository-recorded baseline is 41 tests passing under the pinned environment. The current environment must be checked independently; dependency installation may be unavailable. Some real-data I1/I2 paths are already known to fail (CON-008), so a passing synthetic suite does not close that conflict.

## Per-change checklist

- [ ] Acceptance criterion and non-goals are clear.
- [ ] Relevant tests run; command and actual result recorded.
- [ ] No invariant threshold was loosened.
- [ ] Synthetic, replay, and live evidence are labelled separately.
- [ ] Relevant docs, decisions, conflicts, or history were updated; unrelated logs were not churned.
- [ ] Diff and internal links reviewed.

## Escalation

If evidence cannot resolve a scientific or scope conflict, document it in `../03_research/Conflicts.md`, identify the decision needed, and hand it to the maintainer. Do not block unrelated work that does not depend on the conflict.
