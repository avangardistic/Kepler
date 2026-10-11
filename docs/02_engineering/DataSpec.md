# DataSpec

## L2 Schema

### Binance Message (`depth20@100ms`)
```json
{
  "stream": "btcusdt@depth20@100ms",
  "data": {
    "lastUpdateId": 1234567890,
    "bids": [["100.1", "1.5"], ["100.0", "3.2"], ...],
    "asks": [["100.2", "2.1"], ["100.3", "4.5"], ...]
  }
}
```

## Normalized Fields
| Field | Type | Description |
|------|-----|-------|
| symbol | str | BTCUSDT (upper case) |
| bids | list[[float, float]] | levels as received, best first, price and quantity unmodified |
| asks | list[[float, float]] | same, ascending price |
| ts_exchange_ns | int ns | Exchange time. **0 when the stream provides none** (the `depth20` snapshot payload has no `E` field — see CON-007) |
| ts_local | int ns | Receive time, always set from the local clock |
| seq | int | lastUpdateId of the snapshot; 0 when absent |
| tick_index | int | Arrival ordinal — the tick quantum (TickModel.md). Strictly increasing within a dataset |

Level count is whatever the stream sent (≤ 20). Raw JSON price/quantity strings are decoded to `float64`; nothing else is transformed (`src/fast_l2_client.py`).

## Storage
- Format: Parquet, compression: zstd
- Partition: `symbol=<S>/day=<YYYY-MM-DD>` (UTC day of `ts_local`)
- File naming: `part-NNNN.parquet`, one file per flush, numbering continues across sessions so a reopened store never overwrites existing data
- One row per tick. Columns: `tick_index`, `symbol`, `seq`, `ts_exchange_ns`, `ts_local_ns`, `bid_prices`, `bid_quantities`, `ask_prices`, `ask_quantities` (the four level columns are `List(Float64)`, so level counts may vary per row)
- Writer: `polars` (Implementation.md §2); reader: `src/tick_buffer.py`
- Measured size on the committed fixture (`tests/data/live_2026-10-11/`): 68,090 bytes for 2,785 ticks ≈ 24.5 bytes/tick compressed with 20 levels/side (the capture-time log recorded 26.6 bytes/tick). A 10M-tick dataset therefore projects to roughly 0.25 GB at this rate; compression depends on market activity, so treat the projection as an estimate, not a guarantee
- Replay order: rows sorted by `tick_index` across partitions, so the same dataset always yields the same sequence
- No derived quantities are stored: microprice, mass, imbalance, G and energy are recomputed at replay time (Axiom 1)

## Validation
- bids strictly descending
- asks strictly ascending
- best_bid < best_ask
- All volumes > 0

Validation is **recorded, not enforced**: a tick that fails any rule is still stored and replayed (the client increments `TickStats.invalid_books`). Repairing or dropping it would be a filter (goal.md) and would hide the jump-to-zero case the physics must survive (Falsifiability.md F2).
