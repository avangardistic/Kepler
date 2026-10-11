# Change Report — YYYY-MM-DD

> Copy this template for every PR / session. Policy alignment is mandatory per `docs/QA_Protocol.md` and `docs/Invariants.md`.

## 1. Summary

- **Author(s):**
- **Branch:** `arena/<id>-kepler`
- **Base:** `e777edf` (`main`)
- **Audit date:** YYYY-MM-DD
- **Related task:** T-00x / CON-00x / n/a

One-sentence description of what changed and why:

> e.g. “Deliver Phase-1 tick buffering (T-002); no invariant threshold changed.”

---

## 2. Changes Made

### Code
- [ ] `src/…` —
- [ ] `tests/…` —

### Docs
- [ ] `docs/…` —
- [ ] `README.md` —
- [ ] `requirements.txt` —

### Infra / Tooling
- [ ] `.gitignore` / CI / other —

For each bullet, add the **reasoning** (which ADR / doc / conflict motivated it).

---

## 3. Policy Alignment Checklist

All boxes must be checked before merge. If unchecked, explain in §5.

- [ ] All invariants preserved (`docs/Invariants.md` I1–I7)
- [ ] Test thresholds are **not** loosened (`docs/QA_Protocol.md P3`)
- [ ] `pytest tests/ -v` passes: __ / 41 (or updated count)
- [ ] No external parameters, filters, indicators, or risk management added (`docs/goal.md` constraints)
- [ ] Only raw L2 ticks are used as input; no derived data stored (`docs/DataSpec.md`)
- [ ] Time remains quantised in ticks (`docs/TickModel.md`, `Decisions ADR-006`)
- [ ] Self-induced `G` still derived internally; no magic constants (`Axiom 4`, `Decisions ADR-007 rejected`)
- [ ] Documented in `docs/ResearchLog.md` and `docs/Changelog.md`
- [ ] Conflicts updated in `docs/Conflicts.md` (new or resolved, with status)
- [ ] Decisions updated in `docs/Decisions.md` if an ADR was added / superseded

---

## 4. Tests & Evidence

### Automated tests
```
pytest tests/ -v   # paste tail
```
- New tests: —
- Updated tests: —
- Coverage: offline, deterministic, injected clock/transport where applicable.

### Measurements (if applicable)
| Metric | Before | After | Notes |
|---|---|---|---|
| `integrate` throughput |  |  |  |
| `store write` ticks/s |  |  |  |
| `replay` ticks/s |  |  |  |
| Energy drift (I2) |  |  |  |
| Virial `|<T>/<V>+0.5|` |  |  |  |

### Manual / live runs (if applicable)
- Command: `python -m src.fast_l2_client --ticks 100000 --out data/l2 --base wss://data-stream.binance.vision/stream`
- Result: `captured=… dropped=… out_of_order=… invalid_books=…`

---

## 5. Conflicts & Risks

- **Conflicts introduced:** none / CON-00x (open)
- **Conflicts resolved:** none / CON-00x (resolved, evidence: …)
- **Known limitations / follow-ups:** —
- **Risk if not merged:** —

---

## 6. Related Issues & Docs

- Refs: `docs/Conflicts.md` CON-00x, `docs/FailureModes.md` F0x
- Refs: `docs/Decisions.md` ADR-00x
- Refs: issue #… / PR #…

---

## 7. Reviewer Checklist

- [ ] Invariants table in `docs/Invariants.md` matches test criteria
- [ ] `__all__` policy honoured (internal `_helpers` excluded, public API listed)
- [ ] No silent filtering of ticks (`stats.invalid_books` counted, not dropped)
- [ ] Parquet layout is `symbol=<S>/day=<YYYY-MM-DD>/part-NNNN.parquet`, `zstd`, `List(Float64)`
- [ ] No unbounded memory (`TickBuffer` bounded, flush-based)
- [ ] Double precision still enabled (`jax_enable_x64`) if I2 is relevant
