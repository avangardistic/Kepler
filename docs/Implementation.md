# Implementation

## 1. Architecture
```
L2 WebSocket → Fast Client → Detectors → Physics → MM → Grid → Simulator
```

## 2. Technology Stack
| Layer | Library | Status |
|------|----------|--------|
| Loop | uvloop | optional — POSIX only (ADR-010) |
| WS | websockets | used by `src/fast_l2_client.py` (T-001) |
| JSON | orjson | optional — stdlib fallback (ADR-010) |
| Physics | JAX | used by `src/physics_jax.py` |
| Detectors | numba | reserved (ADR-003, Phase 3 — not implemented) |
| Buffer | polars | used by `src/tick_buffer.py` (T-002), `polars[rtcompat]` where the CPU lacks AVX2 (ADR-011) |

## 3. Folder Structure (as implemented)
```
Kepler/
├── docs/
├── src/
│   ├── fast_l2_client.py   # Phase 1: raw L2 WebSocket ingestion (T-001)
│   ├── tick_buffer.py      # Phase 1: buffer + Parquet store + replay (T-002)
│   └── physics_jax.py      # Phase 2: three-body physics engine
├── tests/
│   ├── test_fast_l2_client.py
│   ├── test_tick_buffer.py
│   └── test_physics.py
└── requirements.txt
```

A later phase may split `src/` into `client/`, `detectors/`, `mm/` and `sim/`
sub-packages; until those modules exist, flat modules avoid empty scaffolding.

## 4. Tick Flow
```python
# Implemented (Phase 1): raw ingestion → bounded buffer → Parquet
client = FastL2Client()
buffer = TickBuffer(L2ParquetStore("data/l2"), flush_rows=50_000)

async for tick in client.stream():        # arrival order, no drops
    buffer.append(tick)                   # auto-flush, bounded memory

# Later phases consume the same ticks from disk:
for state in TickReplay("data/l2").states():
    ...                                   # state_from_l2 → integrate

# Planned (Phase 3–5), not implemented yet:
async for frame in client.pop_batch(512):
    book = parse_book(frame)
    update_detectors(frame, book)                     # T-005
    m_eff = correct_mass(book, detections)            # T-005
    physics.set_state(i, x, m_eff, I, γ)              # Phase 4/5
physics.step()
L = physics.angular_momentum()
quotes = mm.quote_all(physics.state, L)               # T-006
```

## 5. Anti-Patterns
❌ time.sleep in hot path
❌ pandas in hot path
❌ threading.Lock
❌ Unbounded memory

## 6. Testing
- Unit: physics, detectors, mm
- Property: L, Π, bid < ask
- Integration: 1 hour live
