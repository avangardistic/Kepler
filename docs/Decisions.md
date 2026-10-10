# Decisions (ADR)

## ADR-001: Microprice Selection Over Mid
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Microprice is sensitive to order flow imbalance.
**Rejected alternative:** mid (blind to volume).

## ADR-002: JAX for Physics
**Date:** 2025-01
**Status:** Accepted
**Rationale:** JIT + x64 + vmap.
**Rejected alternative:** NumPy (slow), PyTorch (heavy).

## ADR-003: numba for Detection
**Date:** 2025-01
**Status:** Accepted
**Rationale:** 100x faster than pure Python.
**Rejected alternative:** Cython (complex).

## ADR-004: uvloop + orjson
**Date:** 2025-01
**Status:** Accepted
**Rationale:** 2-10x faster.
**Rejected alternative:** asyncio + json (slow).

## ADR-005: No Risk Management
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Risk solved by geometry.
**Rejected alternative:** stop-loss, position limit.

## ADR-006: Time = Tick
**Date:** 2025-01
**Status:** Accepted
**Rationale:** Natural quantization of markets.
**Rejected alternative:** seconds, candles.

## ADR-007: G_DEFAULT = 1e-6 for log-price positions
**Date:** 2026-10-07
**Status:** REJECTED
**Rationale:** VIOLATES Axiom 4 (self-induced gravity without free parameters).
**Rejected alternative:** N/A — this ADR is rejected.
**Rejection rationale:** See CON-001 in Conflicts.md. G must be self-derived from the system geometry, not a magic constant.
**Post-rejection action:** G_eff = 1 / <d²>_t (time-averaged squared distance).

**Note:** A prior documentation pass mistakenly recorded that the virial test I4
threshold had been "loosened to 1e-5" to make tests pass (CON-002). That never
occurred: `test_virial_ratio_convergence` always used the invariant criterion
`|<T>/<V> + 0.5| < 0.2` over a conservative two-body subsystem for 20,000 ticks
with dt = 0.001. CON-002 was a log-writing error, not a threshold change; the
entry has been corrected in Conflicts.md.
