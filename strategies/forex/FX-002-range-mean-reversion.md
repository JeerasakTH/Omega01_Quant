# FX-002 Range Mean Reversion

## Header

- Strategy ID: FX-002
- Name: Range mean reversion with regime filter
- Owner role: Research
- Supporting roles: PM, Quant Dev, QA, Risk, Critic
- Status: research
- Risk bucket: low
- Regime: range, mean reversion

## Research-Only Notice

This is a research-only strategy spec, not a trade recommendation or live deployment approval.

## Hypothesis

When forex pairs are in low-trend range regimes, short-term deviations from a rolling mean revert often enough to justify trades if entries are filtered by volatility, trend strength, and spread.

## Market and Instruments

- Market: Forex
- Symbols: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD
- Broker/data source: Exness MT5
- Timezone assumption: discover from MT5 data inventory before backtesting

## Timeframes

- Entry timeframe: M5 or M15
- Confirmation timeframe: M30
- Context timeframe: H1

## Signals

- Regime filter: ADX below threshold and ATR percentile not elevated.
- Entry signal: price closes outside Bollinger band or z-score threshold, then shows re-entry confirmation.
- Exit signal: return to rolling mean, fixed R, or time stop.
- No-trade filter: strong H1 trend, high spread, news windows, volatility expansion.

## Entry Rules

Long:

- Range filter active.
- Price closes below lower band or below negative z-score threshold.
- Next candle closes back inside band or above prior candle high.

Short:

- Range filter active.
- Price closes above upper band or above positive z-score threshold.
- Next candle closes back inside band or below prior candle low.

## Exit Rules

- Stop loss: beyond recent swing plus buffer or ATR multiple.
- Take profit: rolling mean, mid-band, or fixed R target.
- Time stop: exit after N bars if mean is not reached.
- Invalidating condition: ADX/ATR regime changes to trend or high volatility.

## Position Sizing

- Sizing model: fixed fractional risk.
- Max risk per trade: start research at 0.25%.
- Max simultaneous positions: 2.
- Max symbol exposure: 1 open position per symbol.

## Costs and Execution Assumptions

- Spread: required filter for M5 tests.
- First-pass max spread filter: use M5/M15 symbol-specific limits from `docs/research/mt5-spread-analysis.md`; prefer stricter M5 limits for mean reversion entries.
- Commission: Exness account-specific assumption required.
- Slippage: fixed point and stress scenarios.
- Fill model: next bar open after confirmation close.
- News/event handling: skip high-impact windows after event calendar is available.

## Data Requirements

- OHLCV: M5, M15, M30, H1.
- Spread: strongly preferred for intraday mean reversion.
- Sessions: helpful for avoiding illiquid windows.
- Minimum history: 2-3 years if available.

## Validation Plan

- In-sample period: earliest 60%.
- Out-of-sample period: latest 40%.
- Walk-forward plan: quarterly or semiannual parameter refresh test.
- Symbols: start EURUSD and USDJPY, then expand.
- Benchmarks: random fade entries in same range regime, no-trade baseline.

## Metrics

- Net return, max drawdown, recovery time, profit factor, win rate, average R, trade count, exposure, tail loss, average holding time.

## Kill Criteria

- One large loss erases many small wins.
- Strategy requires widening stops until risk is unacceptable.
- Results vanish when spread is doubled.
- Range filter cannot reliably avoid trend days.

## QA Checklist

- Rolling statistics use past bars only.
- Band/z-score calculations are aligned correctly.
- Spread filter is applied before entry.
- No hidden averaging down.
- Time stop behavior is deterministic.

## Risk Review Questions

- How does the strategy behave during breakout transitions?
- What is the tail loss when ranges fail?
- Does it cluster losses during news or trend days?

## Critic Review Questions

- Is the range filter overfit?
- Are wins mostly small and losses occasional but large?
- Does the strategy survive simple parameter alternatives?
