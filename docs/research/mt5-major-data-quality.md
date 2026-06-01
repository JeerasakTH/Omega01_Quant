# MT5 Major Forex Data Quality Report

Primary mode: Data Engineer + QA

This report summarizes the first deeper MT5/Exness data pull for major forex pairs. The raw CSV files are local-only under `data/raw/mt5/` and are intentionally excluded from git.

## Pull Command

```powershell
.\.venv\Scripts\python.exe -m omega01.cli.mt5_fetch_forex --bars 10000 --report reports\mt5_forex_quality.csv
```

## Symbols

- `EURUSDm`
- `GBPUSDm`
- `USDJPYm`
- `USDCHFm`
- `USDCADm`
- `AUDUSDm`
- `NZDUSDm`

## Timeframes

- `M5`
- `M15`
- `H1`
- `H4`
- `D1`

## Local Outputs

- Raw datasets: `data/raw/mt5/<symbol>/<symbol>_<timeframe>.csv`
- Quality CSV: `reports/mt5_forex_quality.csv`
- Files created: 35 raw CSV files
- Raw CSV size: about 18 MB

## Coverage Summary

| Timeframe | Rows per symbol | Earliest first bar | Latest last bar |
| --- | ---: | --- | --- |
| M5 | 10000 | 2026-04-13T19:50:00+00:00 | 2026-06-01T14:45:00+00:00 |
| M15 | 10000 | 2026-01-06T11:30:00+00:00 | 2026-06-01T14:45:00+00:00 |
| H1 | 10000 | 2024-10-20T23:00:00+00:00 | 2026-06-01T14:00:00+00:00 |
| H4 | 6172 | 2022-08-01T00:00:00+00:00 | 2026-06-01T12:00:00+00:00 |
| D1 | 1199 | 2022-08-01T00:00:00+00:00 | 2026-06-01T00:00:00+00:00 |

## Quality Findings

- Duplicate timestamps: 0 across all pulled datasets.
- Missing OHLC rows: 0 across all pulled datasets.
- Invalid OHLC rows: 0 across all pulled datasets.
- Gap counts are nonzero because the current checker is calendar-unaware and counts weekend/market-close breaks as gaps.

Current gap checks are useful as a rough detector, but they should not be treated as failure until we add a forex trading calendar.

## QA Interpretation

The initial data pull is usable for early research scaffolding, especially for H1/H4/D1 context and prototype tests. Before serious backtest conclusions, improve quality checks so expected forex market closures are not flagged as data gaps.

## Next Actions

1. Add forex calendar-aware gap checks.
2. Decide whether to pull more than 10,000 bars for M5 and M15, because current M5 coverage starts in April 2026.
3. Add spread analysis from the MT5 `spread` column.
4. Create tiny test fixtures from selected clean rows, while keeping full datasets out of git.
5. Start FX-001 feature engineering using H1/H4 context and M15/M30 entries after calendar-aware validation.
