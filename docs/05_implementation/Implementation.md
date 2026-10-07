# Implementation

## 1. معماری
```
L2 WebSocket → Fast Client → Detectors → Physics → MM → Grid → Simulator
```

## 2. پشته فناوری
| لایه | کتابخانه |
|------|----------|
| Loop | uvloop |
| WS | websockets |
| JSON | orjson |
| Physics | JAX |
| Detectors | numba |
| Buffer | polars |

## 3. ساختار پوشه
```
three-body-hft/
├── docs/
├── src/client/, detectors/, physics/, mm/, sim/
├── tests/
└── requirements.txt
```

## 4. جریان tick
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

## 5. ضد-الگوها
❌ time.sleep در hot path
❌ pandas در hot path
❌ threading.Lock
❌ حافظه unbounded

## 6. تست
- Unit: physics, detectors, mm
- Property: L, Π, bid < ask
- Integration: ۱ ساعت زنده
