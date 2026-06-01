# FX-003 London Breakout

## Header

- Strategy ID: FX-003
- Name: London session breakout after Asian range
- Owner role: Research
- Supporting roles: PM, Quant Dev, QA, Risk, Critic
- Status: research
- Risk bucket: medium
- Regime: low volatility to trend

## Research-Only Notice

This is a research-only strategy spec, not a trade recommendation or live deployment approval.

## Hypothesis

After a compressed Asian session range, London liquidity can trigger directional expansion that is tradable if false breakouts, spread, and time-of-day risk are controlled.

## Market and Instruments

- Market: Forex
- Symbols: EURUSD, GBPUSD, EURJPY, GBPJPY, USDJPY
- Broker/data source: Exness MT5
- Timezone assumption: must be mapped before session rules are trusted

## Timeframes

- Entry timeframe: M5 or M15
- Confirmation timeframe: M15
- Context timeframe: H1

## Signals

- Regime filter: Asian range width below ATR percentile threshold.
- Entry signal: London-window break above/below Asian range with close confirmation.
- Exit signal: ATR stop, opposite range break, time stop, or session close.
- No-trade filter: wide Asian range, high spread, pre-news window, already extended move before London.

## Entry Rules

Long:

- Asian range is defined and compressed.
- London window opens.
- Price closes above Asian range high plus buffer.
- Spread is under max threshold.

Short:

- Asian range is defined and compressed.
- London window opens.
- Price closes below Asian range low minus buffer.
- Spread is under max threshold.

## Exit Rules

- Stop loss: opposite side of breakout candle or inside Asian range with ATR cap.
- Take profit: fixed R, ATR target, or trailing stop; compare in research.
- Time stop: exit by end of London window or after N bars.
- Invalidating condition: price closes back inside Asian range after breakout.

## Position Sizing

- Sizing model: fixed fractional risk.
- Max risk per trade: start research at 0.25%-0.50%.
- Max simultaneous positions: 2.
- Max symbol exposure: 1 open position per symbol.

## Costs and Execution Assumptions

- Spread: required because session open spreads may widen.
- Commission: Exness account-specific assumption required.
- Slippage: stress test breakout fills with worse entry.
- Fill model: next bar open after breakout close.
- News/event handling: skip high-impact London/NY event windows.

## Data Requirements

- OHLCV: M5, M15, H1.
- Spread: required before serious report.
- Sessions: Asian and London windows mapped to MT5 server time.
- Minimum history: 3 years if available.

## Validation Plan

- In-sample period: earliest 60%.
- Out-of-sample period: latest 40%.
- Walk-forward plan: yearly session parameter stability check.
- Symbols: start EURUSD, GBPUSD, USDJPY.
- Benchmarks: breakout of random prior range, no-trade baseline.

## Metrics

- Net return, max drawdown, recovery time, profit factor, win rate, average R, trade count, false breakout rate, average slippage stress.

## Kill Criteria

- Edge exists only on one symbol or one year.
- Spread/slippage stress destroys expectancy.
- False breakouts dominate after costs.
- Session timezone uncertainty cannot be resolved.

## QA Checklist

- Session windows are timezone documented.
- Asian range uses completed bars only.
- Breakout signal waits for close confirmation.
- Spread and news filters are applied before entry.
- Time stop exits are deterministic.

## Risk Review Questions

- What happens on failed breakouts during high-impact news?
- Does correlation across GBP/EUR pairs stack risk?
- Is stop distance stable or too variable?

## Critic Review Questions

- Is London breakout a crowded pattern with no remaining edge?
- Are results sensitive to exact session times?
- Does execution realism erase the backtest edge?
