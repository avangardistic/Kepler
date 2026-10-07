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
