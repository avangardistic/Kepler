# Tool and Language Selection — Research Note

**Date:** 2026-10-10
**Scope:** Physics engine (`src/physics_jax.py`) and its heavy computations (Phase 2 and Phase 5 of roadmap.md).
**Related:** ADR-002 (JAX), ADR-003 (numba), ADR-009 (decision).

## 1. Question
Is Python + JAX fast enough for the physics engine, or should a heavy part move to another language or tool?

## 2. Requirements from the documents
- roadmap.md Phase 5: 10 million ticks.
- Invariants.md / Physics.md: float64 precision is required for I2 (relative energy drift < 1e-9); see ADR-002 "JIT + x64 + vmap".
- Implementation.md §5: no `time.sleep` in the hot path, no unbounded memory.
- No explicit wall-clock limit for the simulation is given in the documents.

## 3. Candidates
| Option | Pros | Cons |
|---|---|---|
| Python + JAX (x64), `lax.scan` | Already in use (ADR-002); autodiff and vmap; float64 | JIT compile time; GPU not needed here |
| NumPy loops | Simple | Slow; no JIT |
| numba | Fast loops; ADR-003 choice for detectors | Not used for physics yet |
| C++ / Rust / Julia | Maximum speed | New toolchain; conflicts with ADR-002; more code to verify |

## 4. Measurements (sandbox: 2 CPU cores, 3 GB RAM, CPU only)
| Experiment | Result |
|---|---|
| Steady-state `symplectic_step` in `lax.scan`, 3 bodies, 1 M ticks | 0.31 s (≈ 3.25 M ticks/s) |
| Same, 10 M ticks | 3.01 s (≈ 3.32 M ticks/s) |
| Full test suite (9 tests, float64) | ≈ 9 s wall clock, including JIT compilation |
| `integrate` 200 k ticks, 2 bodies | ≈ 0.5 s |

## 5. Decision by 5 Whys
**Problem:** Should the physics engine switch to another language?

1. **Why consider a change?** Concern that Python would be too slow for the 10 M-tick simulation (roadmap Phase 5).
2. **Why would Python be too slow?** Interpreter overhead in per-tick loops, if the loop is not compiled.
3. **Why is that not the case here?** The tick loop is compiled once with `lax.scan` (JIT), so the work per tick runs as compiled XLA code, not as Python bytecode.
4. **Why is that known and not assumed?** Measured in §4: ≈ 3.3 M ticks/s, so 10 M ticks ≈ 3 s on this sandbox.
5. **Why is no other language needed?** No document sets a time limit that 3 s violates; ADR-002 already fixes JAX, and rewriting in another language would add verification cost without a measured need.

**Root cause:** the performance concern was a hypothesis, not a measured bottleneck.

**Decision:** Python + JAX (float64) for the physics engine (ADR-009). numba stays for detectors (ADR-003).

## 6. Revisit conditions
- Live WebSocket ingestion (Phase 1) or the market-maker loop (Phase 4) show a measured bottleneck in Python.
- The Phase 5 requirement gains an explicit wall-clock limit.
- Measurements on the target hardware differ significantly from the sandbox numbers above.
