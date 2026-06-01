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
- Gap checks now use a simple Exness-oriented forex calendar: Friday close around 21:00 UTC, Sunday reopen around 21:00 UTC outside winter, and Sunday reopen around 22:00 UTC in winter.
- Common year-end closures around Christmas and New Year are treated as expected closures.
- H4 and D1 pass for all seven major pairs.
- Intraday timeframes still show unexpected open-market gaps and need inspection before serious backtests.

| Timeframe | Passed symbols | Total symbols | Gap range |
| --- | ---: | ---: | --- |
| M5 | 0 | 7 | 7-16 |
| M15 | 0 | 7 | 2-3 |
| H1 | 0 | 7 | 2 |
| H4 | 7 | 7 | 0 |
| D1 | 7 | 7 | 0 |

Gap audit totals:

| Timeframe | Gap events | Missing open bars |
| --- | ---: | ---: |
| M5 | 85 | 97 |
| M15 | 15 | 37 |
| H1 | 14 | 14 |
| H4 | 0 | 0 |
| D1 | 0 | 0 |

## QA Interpretation

The initial data pull is usable for early research scaffolding and H4/D1 context. Intraday datasets need a gap policy before serious backtest conclusions. The remaining H1/M15 gaps mostly cluster around late-February/early-March session changes and Sunday reopen timing; M5 has more small reopen/session-boundary gaps.

## Next Actions

1. Decide gap policy for intraday research: drop affected sessions, forward-fill nothing, and block entries around gap intervals.
2. Decide whether to pull more than 10,000 bars for M5 and M15, because current M5 coverage starts in April 2026.
3. Add spread analysis from the MT5 `spread` column.
4. Create tiny test fixtures from selected clean rows, while keeping full datasets out of git.
5. Start FX-001 feature engineering using H4/D1 context first, and use H1/M15 only with gap-aware entry blocking.

The first spread analysis is summarized in `mt5-spread-analysis.md`.
