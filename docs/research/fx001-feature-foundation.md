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
  - `detect_ema_pullback`
  - `confirm_pullback_resume`
  - `evaluate_fx001_signal`
  - `ExitLevels`
  - `generate_exit_levels`
- `omega01.data.alignment`
  - `align_completed_higher_timeframe`

## What This Supports

- H1/H4 EMA slope classification.
- Price-on-trend-side checks.
- H1/H4 trend alignment into `long`, `short`, or `none`.
- ATR feature creation for later stop and volatility logic.
- Spread and recent-gap entry blocking.
- Completed higher timeframe feature alignment without lookahead.
- Pullback-to-EMA-zone detection.
- Pullback resume confirmation for long and short setups.
- First complete signal evaluator returning `long`, `short`, or `none`.
- Stop-loss and take-profit generation using swing/ATR rules.

## What Is Not Implemented Yet

- Backtest execution engine.
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

1. Add gap-aware signal blocking from actual gap audit intervals.
2. Add a minimal vectorized research backtest for FX-001 only.
3. Run the first EURUSDm H1/H4/M15 research pass.
4. Send results through QA, Risk, and Critic review.
