# Task Queue

## Status: Active

> **Sync note (2026-10-10).** T-003 and T-004 were completed in code and tests
> but had never been moved out of "Open". They are now recorded under
> "Completed" with their verification evidence. No code was changed by this
> sync; `pytest tests/ -v` still reports 9 passed.

> **Sync note (2026-10-11).** T-001 and T-002 are delivered (Phase 1).
> `pytest tests/ -v` → **41 passed** (9 physics + 17 client + 15 storage).
> One new open conflict, CON-008, was raised from real replayed data: see
> `docs/Conflicts.md` and `docs/FailureModes.md` F10.

## Open

### T-005 [Phase 3] [High]
- **Title:** detectors_numba.py
- **Input:** Detectors.md
- **Output:** Iceberg + Spoof
- **Criterion:** F1 > 0.8 on synthetic data
- **Blocked by:** T-001, T-002 (needs recorded L2 ticks)

### T-006 [Phase 4] [High]
- **Title:** market_maker.py
- **Input:** MarketMaking.md
- **Output:** quote_all
- **Criterion:** bid < ask always
- **Blocked by:** T-001, T-002 (needs recorded L2 ticks)

### T-007 [Phase 5] [High]
- **Title:** simulation_live_v3
- **Input:** All
- **Output:** 10M tick simulation
- **Criterion:** Pi > 0 with 95% CI
- **Blocked by:** T-001 … T-006

## In Progress
(Empty)

## Completed
- [x] T-000 [Phase 0] Generate all docs
- [x] T-003 [Phase 2] physics_jax.py — `src/physics_jax.py` implements
      `symplectic_step` (velocity Verlet) and `integrate` (`lax.scan`).
      Verified 2026-10-10 with jax 0.10.2 / pytest 9.1.1 on Python 3.11:
      `pytest tests/ -v` → 9 passed.
      Criterion re-checked: I1 angular momentum bounded, I2 relative energy
      drift < 1e-9 (requires the x64 flag set in code per ADR-002).
- [x] T-004 [Phase 2] Invariant tests — `tests/test_physics.py` (9 tests):
      angular momentum (zero at rest, bounded over 10k ticks, cumulative
      series recorded), energy conservation, virial ratio (I4), imbalance
      bound (I6), zero-depth freeze, ε-softening, determinism.
      All pass in the default configuration.

- [x] T-001 [Phase 1] fast_l2_client — `src/fast_l2_client.py`: raw
      `depth20@100ms` snapshot client for btcusdt/ethusdt/solusdt, pull-based
      (no drops by construction), per-symbol sequence checks, no filtering.
      Verified 2026-10-11 (jax 0.10.2 / pytest 9.1.1 / Python 3.11):
      `pytest tests/ -v` → 41 passed. Acceptance: **100 000 ticks,
      `dropped == 0`, `out_of_order == 0`** (`test_acceptance_100k_ticks_without_drop`).
      Live smoke run 2026-10-11 via `data-stream.binance.vision`: 2 785 real
      ticks in 120 s, 20 levels/side, 0 invalid books, 0 drops
      (the main `stream.binance.com` domain answers HTTP 451 from this
      network — see ADR-011 / ResearchLog).
- [x] T-002 [Phase 1] tick_buffer + Parquet + replay — `src/tick_buffer.py`:
      bounded `TickBuffer`, `L2ParquetStore` (Parquet/zstd, `symbol/day`
      partitions, `part-NNNN` continuation), `TickReplay` (deterministic
      `ticks()` / `states()` → `state_from_l2`), `parquet_codecs()` for
      dependency-free codec verification. Criterion verified: identical tick
      sequence and identical `integrate` trajectory on repeated replay.
      Measured: write 6 837 ticks/s, replay 24 244 ticks/s, 26.6 B/tick.

## Prioritization
1. **CON-008** (open, escalated): without a decision, Phase 3–5 run on a
   model whose I1/I2 fail on real replay. It is now the highest-value item
   even though detectors consume recorded ticks.
2. T-005 (detection) — data is now available on disk.
3. T-006 (MM)
4. T-007 (integration)

## Known follow-ups (not tasks yet)
- **CON-008 (open):** I1/I2 fail on real L2 replay at `dt = 1`; four candidate
  directions listed in Conflicts.md. Needs a human decision + ADR before
  Phase 5.
- **Performance:** `TickReplay.states()` costs 13.1 ms per tick (76 states/s,
  measured) because `state_from_l2` runs outside jit. Phase 3–5 loops that need
  a state per tick must jit/vmap the construction (ADR-009 revisit trigger).
- Live acceptance run for T-001 at full scale: 3 assets × ~10 ticks/s means
  100 000 live ticks take ≈ 55 min of wall clock. Only the offline 100 000-tick
  run and a 120 s live smoke run have been performed; run
  `python -m src.fast_l2_client --ticks 100000 --out data/l2` to complete it.
- Running time-average of ⟨d²⟩ for the self-induced coupling: `integrate`
  currently fixes `G` from the initial state (see Conflicts.md CON-005,
  open remark). Needs a decision before Phase 5.
- Measure the residual of the rigid-rotation embedding for N ≥ 3 (ADR-008):
  now measured on real data (F10: energy drift 1.54 at dt = 1) and folded into
  CON-008.
- `docs/Changelog.md` entries v0.2.0–v0.5.0 describe modules that are not in
  the repository; they are planned, not delivered. See roadmap.md.
- Documentation hygiene: six docs were cyclically mis-filed by commit
  `829a846` (CON-006). Any future script that rewrites docs must be checked by
  reading the first heading of each file.
