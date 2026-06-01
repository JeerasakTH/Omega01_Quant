# FX-001 Feature Engineering Foundation

Primary mode: Quant Dev + QA

This document records the first reusable feature foundation for FX-001 Multi-Timeframe Trend Following. It is not a backtest and does not generate trade recommendations yet.

## Implemented Modules

- `omega01.features.technical`
  - `add_ema`
  - `add_atr`
  - `slope_direction`
- `omega01.strategies.fx001`
  - `TrendState`
  - `SpreadFilter`
  - `build_trend_state`
  - `align_trends`
  - `is_entry_allowed`

## What This Supports

- H1/H4 EMA slope classification.
- Price-on-trend-side checks.
- H1/H4 trend alignment into `long`, `short`, or `none`.
- ATR feature creation for later stop and volatility logic.
- Spread and recent-gap entry blocking.

## What Is Not Implemented Yet

- Pullback detection toward EMA zone.
- Entry candle confirmation.
- Stop-loss and take-profit generation.
- Backtest execution engine.
- Higher timeframe to lower timeframe alignment.
- Gap-aware signal blocking from actual gap audit intervals.

## Verification

Tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_fx001_features.py
```

Expected:

```text
6 passed
```

## Next Actions

1. Add timeframe alignment utilities so H1/H4 completed-bar features can be joined to M15 entries without lookahead.
2. Add pullback-to-EMA-zone detection.
3. Add signal confirmation logic for long and short entries.
4. Add a minimal vectorized research backtest for FX-001 only.
