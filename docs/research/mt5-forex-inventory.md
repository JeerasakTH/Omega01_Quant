# MT5 Forex Inventory

Primary mode: Data Engineer

This document summarizes the first forex symbol inventory pulled from the local Exness MT5 terminal. The generated CSV is local-only at `reports/mt5_forex_inventory.csv` and is intentionally not committed.

## Inventory Run

- Date: 2026-06-01
- Terminal: already-open Exness MT5 terminal via `MetaTrader5.initialize()`
- Command:

```powershell
.\.venv\Scripts\python.exe -m omega01.cli.mt5_forex_inventory --timeframes M5,M15,H1,H4,D1 --bars 1000 --out reports\mt5_forex_inventory.csv
```

- Result: 28 forex symbols, 140 symbol-timeframe rows.
- Note: passing an explicit `terminal64.exe` path timed out in this environment. Initializing against the already-open terminal worked.

## Forex Symbols Found

All discovered symbols use the Exness `m` suffix.

| Symbol | Base symbol |
| --- | --- |
| AUDCADm | AUDCAD |
| AUDCHFm | AUDCHF |
| AUDJPYm | AUDJPY |
| AUDNZDm | AUDNZD |
| AUDUSDm | AUDUSD |
| CADCHFm | CADCHF |
| CADJPYm | CADJPY |
| CHFJPYm | CHFJPY |
| EURAUDm | EURAUD |
| EURCADm | EURCAD |
| EURCHFm | EURCHF |
| EURGBPm | EURGBP |
| EURJPYm | EURJPY |
| EURNZDm | EURNZD |
| EURUSDm | EURUSD |
| GBPAUDm | GBPAUD |
| GBPCADm | GBPCAD |
| GBPCHFm | GBPCHF |
| GBPJPYm | GBPJPY |
| GBPNZDm | GBPNZD |
| GBPUSDm | GBPUSD |
| NZDCADm | NZDCAD |
| NZDCHFm | NZDCHF |
| NZDJPYm | NZDJPY |
| NZDUSDm | NZDUSD |
| USDCADm | USDCAD |
| USDCHFm | USDCHF |
| USDJPYm | USDJPY |

## Timeframe Coverage From 1000-Bar Probe

| Timeframe | Symbols with data | Earliest first bar | Latest last bar |
| --- | ---: | --- | --- |
| M5 | 28 | 2026-05-27T03:00:00+00:00 | 2026-06-01T14:40:00+00:00 |
| M15 | 28 | 2026-05-18T04:15:00+00:00 | 2026-06-01T14:30:00+00:00 |
| H1 | 28 | 2026-04-02T23:00:00+00:00 | 2026-06-01T14:00:00+00:00 |
| H4 | 28 | 2025-10-15T20:00:00+00:00 | 2026-06-01T12:00:00+00:00 |
| D1 | 28 | 2023-03-21T00:00:00+00:00 | 2026-06-01T00:00:00+00:00 |

## Initial Research Universe Update

Use the actual Exness `m` suffix symbols in data work. The first-pass research basket should start with liquid majors and key crosses:

- Majors: `EURUSDm`, `GBPUSDm`, `USDJPYm`, `USDCHFm`, `USDCADm`, `AUDUSDm`, `NZDUSDm`
- JPY crosses: `EURJPYm`, `GBPJPYm`, `AUDJPYm`, `CADJPYm`, `CHFJPYm`, `NZDJPYm`
- EUR/GBP/AUD/NZD crosses: `EURGBPm`, `EURAUDm`, `EURNZDm`, `GBPAUDm`, `GBPNZDm`, `AUDNZDm`

## Next Data Tasks

1. Pull deeper history for the first-pass majors on M5, M15, H1, H4, and D1.
2. Measure whether MT5 exposes spread history reliably for these symbols.
3. Confirm MT5 server timezone by comparing recent bar timestamps with known market session boundaries.
4. Create small committed fixtures for tests, not full datasets.
5. Build data quality checks for gaps, duplicates, timezone consistency, and missing OHLC values.
