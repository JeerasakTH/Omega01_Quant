# FX-004 ATR Volatility Breakout

## Header

- Strategy ID: FX-004
- Name: ATR volatility breakout
- Owner role: Research
- Supporting roles: PM, Quant Dev, QA, Risk, Critic
- Status: research
- Risk bucket: medium
- Regime: high volatility, trend

## Research-Only Notice

This is a research-only strategy spec, not a trade recommendation or live deployment approval.

## Hypothesis

When realized volatility expands and price breaks a recent range, continuation can be captured with ATR-based stops and exits, provided spread and whipsaw risk are controlled.

## Market and Instruments

- Market: Forex
- Symbols: EURUSD, GBPUSD, USDJPY, GBPJPY, EURJPY
- Broker/data source: Exness MT5
- Timezone assumption: discover from MT5 data inventory before backtesting

## Timeframes

- Entry timeframe: M5, M15, or H1
- Confirmation timeframe: M15 or H1
- Context timeframe: H4

## Signals

- Regime filter: ATR percentile rising or current ATR above rolling threshold.
- Entry signal: price breaks recent high/low range with volatility expansion.
- Exit signal: trailing ATR stop, fixed R, or volatility contraction.
- No-trade filter: spread spike, immediate post-news instability, conflicting H4 structure.

## Entry Rules

Long:

- ATR expansion condition active.
- Price closes above recent N-bar high plus buffer.
- H1/H4 context is not strongly bearish.

Short:

- ATR expansion condition active.
- Price closes below recent N-bar low minus buffer.
- H1/H4 context is not strongly bullish.

## Exit Rules

- Stop loss: ATR multiple from entry or opposite side of breakout range.
- Take profit: trailing ATR stop or fixed R target.
- Time stop: exit if breakout does not continue within N bars.
- Invalidating condition: close back inside breakout range with volatility contraction.

## Position Sizing

- Sizing model: volatility-adjusted fixed fractional risk.
- Max risk per trade: start research at 0.25%-0.50%.
- Max simultaneous positions: 3.
- Max symbol exposure: 1 open position per symbol.

## Costs and Execution Assumptions

- Spread: filter and stress test required.
- First-pass max spread filter: use entry-timeframe symbol-specific limits from `docs/research/mt5-spread-analysis.md`; stress with stricter and looser thresholds because volatility breakouts may coincide with widening spreads.
- Commission: Exness account-specific assumption required.
- Slippage: breakout slippage stress is required.
- Fill model: next bar open after signal close.
- News/event handling: separate tests with and without blackout windows.

## Data Requirements

- OHLCV: M5, M15, H1, H4.
- Spread: preferred, required before promotion.
- Sessions: optional for first pass, useful for later filters.
- Minimum history: 3 years if available.

## Validation Plan

- In-sample period: earliest 60%.
- Out-of-sample period: latest 40%.
- Walk-forward plan: evaluate ATR threshold stability by year.
- Symbols: start EURUSD, GBPUSD, USDJPY.
- Benchmarks: simple channel breakout without ATR filter, no-trade baseline.

## Metrics

- Net return, max drawdown, recovery time, profit factor, win rate, average R, trade count, average holding time, whipsaw rate.

## Kill Criteria

- Whipsaws create unacceptable drawdown.
- Results depend on one ATR threshold.
- Slippage stress removes expectancy.
- Strategy overtrades high-spread periods.

## QA Checklist

- ATR uses prior completed bars only.
- Breakout ranges do not include the signal bar incorrectly.
- Slippage stress is included.
- Volatility filter is calculated without future data.
- Time stop and trailing stop are reproducible.

## Risk Review Questions

- How large are losses during false volatility expansion?
- Does the strategy stack risk across correlated pairs?
- How sensitive is DD to slippage stress?

## Critic Review Questions

- Is this just buying volatility after the move already happened?
- Does it survive different range lengths and ATR windows?
- Does the edge exist outside a few crisis periods?
