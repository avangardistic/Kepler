# DataSpec

## اسکیمای L2

### پیام Binance (`depth20@100ms`)
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

## فیلدهای نرمال‌شده
| فیلد | نوع | توضیح |
|------|-----|-------|
| symbol | str | BTCUSDT |
| bids | list[[float, float]] | ۲۰ سطح |
| asks | list[[float, float]] | ۲۰ سطح |
| ts_exchange | int ns | زمان صرافی |
| ts_local | int ns | زمان دریافت |
| seq | int | lastUpdateId |

## ذخیره‌سازی
- فرمت: Parquet
- فشرده‌سازی: zstd
- پارتیشن: symbol / day
- اندازه تخمینی: ۱ GB برای ۱۰M tick

## اعتبارسنجی
- bids strictly descending
- asks strictly ascending
- best_bid < best_ask
- همه حجم‌ها > 0
