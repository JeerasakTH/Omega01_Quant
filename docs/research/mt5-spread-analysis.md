# MT5 Spread Analysis

Primary mode: Data Engineer + Risk

This report summarizes spread distributions from the local Exness MT5 major-pair datasets. The generated CSV is local-only at `reports/mt5_spread_analysis.csv` and is intentionally not committed.

## Command

```powershell
.\.venv\Scripts\python.exe -m omega01.cli.mt5_analyze_spread --out reports\mt5_spread_analysis.csv
```

## Interpretation

MT5 `spread` values are broker-provided integer points. These are used as research filters first; final EA settings must confirm point/pip conversion against the account symbol specification before live use.

The initial recommended max spread is:

```text
max(p95 spread, median spread + 2 points)
```

This is intentionally conservative enough to block obvious spread spikes while not overfitting to rare max values.

## M15 Recommended Max Spread

M15 is the first likely entry timeframe for FX-001 and part of the first-pass intraday research stack.

| Symbol | Median | P95 | Recommended max spread |
| --- | ---: | ---: | ---: |
| EURUSDm | 8 | 8 | 10 |
| AUDUSDm | 9 | 9 | 11 |
| GBPUSDm | 10 | 10 | 12 |
| USDJPYm | 10 | 10 | 12 |
| USDCHFm | 13 | 13 | 15 |
| USDCADm | 15 | 16 | 17 |
| NZDUSDm | 18 | 18 | 20 |

## Full Timeframe Summary

| Symbol | Timeframe | Median | P95 | Recommended max spread | Max observed |
| --- | --- | ---: | ---: | ---: | ---: |
| EURUSDm | M5 | 8 | 8 | 10 | 191 |
| EURUSDm | M15 | 8 | 8 | 10 | 192 |
| EURUSDm | H1 | 9 | 9 | 11 | 160 |
| EURUSDm | H4 | 8 | 10 | 10 | 167 |
| EURUSDm | D1 | 8 | 10 | 10 | 156 |
| GBPUSDm | M5 | 10 | 10 | 12 | 296 |
| GBPUSDm | M15 | 10 | 10 | 12 | 296 |
| GBPUSDm | H1 | 10 | 11 | 12 | 236 |
| GBPUSDm | H4 | 10 | 12 | 12 | 184 |
| GBPUSDm | D1 | 10 | 12 | 12 | 184 |
| USDJPYm | M5 | 10 | 10 | 12 | 350 |
| USDJPYm | M15 | 10 | 10 | 12 | 158 |
| USDJPYm | H1 | 10 | 10 | 12 | 158 |
| USDJPYm | H4 | 10 | 11 | 12 | 350 |
| USDJPYm | D1 | 10 | 11 | 12 | 350 |
| USDCHFm | M5 | 13 | 13 | 15 | 300 |
| USDCHFm | M15 | 13 | 13 | 15 | 300 |
| USDCHFm | H1 | 13 | 13 | 15 | 264 |
| USDCHFm | H4 | 12 | 14 | 14 | 406 |
| USDCHFm | D1 | 12 | 14 | 14 | 406 |
| USDCADm | M5 | 14 | 16 | 16 | 130 |
| USDCADm | M15 | 15 | 16 | 17 | 122 |
| USDCADm | H1 | 15 | 17 | 17 | 164 |
| USDCADm | H4 | 15 | 22 | 22 | 310 |
| USDCADm | D1 | 15 | 22 | 22 | 310 |
| AUDUSDm | M5 | 9 | 9 | 11 | 232 |
| AUDUSDm | M15 | 9 | 9 | 11 | 232 |
| AUDUSDm | H1 | 9 | 9 | 11 | 114 |
| AUDUSDm | H4 | 11 | 14 | 14 | 218 |
| AUDUSDm | D1 | 11 | 14 | 14 | 218 |
| NZDUSDm | M5 | 14 | 14 | 16 | 330 |
| NZDUSDm | M15 | 18 | 18 | 20 | 330 |
| NZDUSDm | H1 | 17 | 18 | 19 | 178 |
| NZDUSDm | H4 | 17 | 20 | 20 | 443 |
| NZDUSDm | D1 | 17 | 20 | 20 | 443 |

## Research Implications

- Prefer `EURUSDm`, `AUDUSDm`, `GBPUSDm`, and `USDJPYm` for first intraday prototypes.
- Treat `USDCADm` and `NZDUSDm` as higher-cost instruments in intraday tests.
- Max observed spreads are much larger than p95, so every intraday strategy needs a max-spread entry filter.
- H4/D1 context filters are less sensitive to spread, but entry execution still needs the entry-timeframe spread filter.

## Proposed First-Pass Filters

- FX-001 M15/M30 entries: use symbol-specific recommended max spread from M15.
- FX-002 M5/M15 mean reversion: start with M5/M15 recommended max spread and stress stricter filters.
- FX-003 London breakout: use recommended max spread plus separate session-open spike analysis before promotion.
- FX-004 volatility breakout: use recommended max spread and slippage stress because breakouts may occur during spread widening.

## Next Actions

1. Add spread filter fields to the first five strategy specs.
2. Add session-specific spread analysis for London open, New York open, rollover, and Sunday reopen.
3. Add point/pip metadata from MT5 symbol info before presenting cost assumptions in pips.
