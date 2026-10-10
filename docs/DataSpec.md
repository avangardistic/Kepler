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
| symbol | str | BTCUSDT |
| bids | list[[float, float]] | 20 levels |
| asks | list[[float, float]] | 20 levels |
| ts_exchange | int ns | Exchange time |
| ts_local | int ns | Receive time |
| seq | int | lastUpdateId |

## Storage
- Format: Parquet
- Compression: zstd
- Partition: symbol / day
- Estimated size: 1 GB for 10M ticks

## Validation
- bids strictly descending
- asks strictly ascending
- best_bid < best_ask
- All volumes > 0
