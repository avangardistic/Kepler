# Implementation

## 1. Architecture
```
L2 WebSocket → Fast Client → Detectors → Physics → MM → Grid → Simulator
```

## 2. Technology Stack
| Layer | Library |
|------|----------|
| Loop | uvloop |
| WS | websockets |
| JSON | orjson |
| Physics | JAX |
| Detectors | numba |
| Buffer | polars |

## 3. Folder Structure
```
three-body-hft/
├── docs/
├── src/client/, detectors/, physics/, mm/, sim/
├── tests/
└── requirements.txt
```

## 4. Tick Flow
```python
while running:
    frames = client.pop_batch(512)
    for frame in frames:
        book = parse_book(frame)
        update_detectors(frame, book)
        m_eff = correct_mass(book, detections)
        physics.set_state(i, x, m_eff, I, γ)
    physics.step()
    L = physics.angular_momentum()
    quotes = mm.quote_all(physics.state, L)
    grid = place_grid(quotes, books)
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
