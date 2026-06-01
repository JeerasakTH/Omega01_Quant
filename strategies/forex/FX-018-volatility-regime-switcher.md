# FX-018 Volatility Regime Switcher

## Header

- Strategy ID: FX-018
- Name: Volatility regime switcher
- Owner role: Research
- Supporting roles: PM, Quant Dev, QA, Risk, Critic
- Status: research
- Risk bucket: medium
- Regime: multi-regime meta-layer

## Research-Only Notice

This is a research-only strategy spec, not a trade recommendation or live deployment approval.

## Hypothesis

Forex strategies perform better when trade selection changes by volatility and trend regime, so a meta-layer that chooses trend, range, or no-trade mode can improve portfolio stability.

## Market and Instruments

- Market: Forex
- Symbols: all first-pass liquid symbols after data inventory
- Broker/data source: Exness MT5
- Timezone assumption: discover from MT5 data inventory before backtesting

## Timeframes

- Entry timeframe: strategy-dependent
- Confirmation timeframe: M15 or H1
- Context timeframe: H1, H4, D1

## Signals

- Regime filter: ATR percentile, ADX, rolling return volatility, and range compression/expansion.
- Entry signal: none by itself; routes to trend, range, breakout, or no-trade mode.
- Exit signal: strategy-dependent or mode invalidation.
- No-trade filter: ambiguous regime, high spread, insufficient data, event windows.

## Entry Rules

Trend mode:

- ATR not compressed.
- ADX or slope indicates directional persistence.
- Enable FX-001 or FX-004 style strategies.

Range mode:

- ADX low.
- ATR stable or declining.
- Enable FX-002 style strategies.

No-trade mode:

- Spread elevated.
- Regime conflicts.
- News/event window active.
- Volatility too unstable for current model.

## Exit Rules

- Stop loss: strategy-dependent.
- Take profit: strategy-dependent.
- Time stop: strategy-dependent.
- Invalidating condition: regime changes against active strategy class.

## Position Sizing

- Sizing model: allocation multiplier by regime confidence.
- Max risk per trade: inherited from active strategy, capped by meta-layer.
- Max simultaneous positions: portfolio-level cap required.
- Max symbol exposure: portfolio-level cap required.

## Costs and Execution Assumptions

- Spread: meta-layer can block trading under high spread.
- First-pass max spread filter: inherit symbol-specific limits from `docs/research/mt5-spread-analysis.md` and allow the meta-layer to force no-trade mode above those limits.
- Commission: inherited from strategy assumptions.
- Slippage: inherited plus regime stress tests.
- Fill model: inherited from active strategy.
- News/event handling: blackout mode by default once event calendar exists.

## Data Requirements

- OHLCV: M15, H1, H4, D1.
- Spread: required for no-trade filters.
- Sessions: useful for session-aware regime labels.
- Minimum history: 3 years if available.

## Validation Plan

- In-sample period: earliest 60%.
- Out-of-sample period: latest 40%.
- Walk-forward plan: yearly threshold stability and mode confusion analysis.
- Symbols: start EURUSD, GBPUSD, USDJPY.
- Benchmarks: each child strategy without regime switcher, always-on baseline.

## Metrics

- Net return, max drawdown, recovery time, profit factor, exposure reduction, avoided-loss analysis, missed-profit analysis, mode accuracy proxy.

## Kill Criteria

- Meta-layer reduces returns without reducing drawdown.
- Mode labels are unstable across symbols or years.
- Thresholds are too fragile.
- It mostly curve-fits child strategy selection.

## QA Checklist

- Regime labels use only past completed bars.
- Child strategy enable/disable decisions are timestamp-aligned.
- No-trade periods are recorded explicitly.
- Comparison against always-on child strategies is reproducible.
- Missing higher timeframe data blocks trades instead of filling forward unsafely.

## Risk Review Questions

- Does the switcher actually reduce drawdown and exposure?
- Can mode changes create concentrated exits or entries?
- How should allocation change when confidence is low?

## Critic Review Questions

- Is the regime model just overfit threshold logic?
- Does it add complexity without robust improvement?
- Does it miss the best trades while avoiding only obvious bad periods?
