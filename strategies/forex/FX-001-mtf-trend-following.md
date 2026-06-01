# FX-001 Multi-Timeframe Trend Following

## Header

- Strategy ID: FX-001
- Name: Conservative multi-timeframe trend following
- Owner role: Research
- Supporting roles: PM, Quant Dev, QA, Risk, Critic
- Status: research
- Risk bucket: low
- Regime: trend

## Research-Only Notice

This is a research-only strategy spec, not a trade recommendation or live deployment approval.

## Hypothesis

Major forex pairs show short-to-medium-term continuation when H1/H4 direction agrees and lower timeframe pullbacks resolve back in the higher timeframe direction.

## Market and Instruments

- Market: Forex
- Symbols: EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURJPY, GBPJPY
- Broker/data source: Exness MT5
- Timezone assumption: discover from MT5 data inventory before backtesting

## Timeframes

- Entry timeframe: M15 or M30
- Confirmation timeframe: H1
- Context timeframe: H4

## Signals

- Trend filter: H1 and H4 EMA slope agree, with price on the same side of the selected EMA.
- Entry signal: pullback toward EMA zone followed by close back in trend direction.
- Exit signal: ATR stop, opposite structure break, or time stop.
- No-trade filter: high spread, major news window, conflicting H1/H4 trend.
- Implementation note: first reusable feature foundation is documented in `docs/research/fx001-feature-foundation.md`.

## Entry Rules

Long:

- H4 trend is up.
- H1 trend is up.
- M15 or M30 pulls back toward EMA zone.
- Entry candle closes above prior minor swing or above pullback candle high.

Short:

- H4 trend is down.
- H1 trend is down.
- M15 or M30 pulls back toward EMA zone.
- Entry candle closes below prior minor swing or below pullback candle low.

## Exit Rules

- Stop loss: below/above pullback swing or ATR multiple, whichever is farther.
- Take profit: fixed R target or trailing ATR; compare both in research.
- Time stop: exit if no favorable movement after N entry timeframe bars.
- Invalidating condition: H1 trend filter flips against position.

## Position Sizing

- Sizing model: fixed fractional risk.
- Max risk per trade: start research at 0.25%-0.50%.
- Max simultaneous positions: 3 across all pairs.
- Max symbol exposure: 1 open position per symbol.

## Costs and Execution Assumptions

- Spread: use MT5 spread if available; otherwise model conservative fixed and stress spread.
- First-pass max spread filter: M15 entries use symbol-specific limits from `docs/research/mt5-spread-analysis.md` (`EURUSDm` 10, `GBPUSDm` 12, `USDJPYm` 12, `AUDUSDm` 11, `USDCHFm` 15, `USDCADm` 17, `NZDUSDm` 20 points).
- Commission: Exness account-specific assumption required before serious report.
- Slippage: start with 0.1-0.3 ATR fraction stress test or fixed point assumptions.
- Fill model: next bar open after signal close for conservative research.
- News/event handling: skip scheduled high-impact windows once calendar integration exists; before that, label limitation.

## Data Requirements

- OHLCV: M15, M30, H1, H4.
- Spread: preferred, required before promotion.
- Sessions: optional for first pass.
- Minimum history: 3 years if available.

## Validation Plan

- In-sample period: earliest 60% of available clean history.
- Out-of-sample period: latest 40%.
- Walk-forward plan: yearly rolling evaluation after first prototype.
- Symbols: start EURUSD, GBPUSD, USDJPY; expand if stable.
- Benchmarks: buy-and-hold direction proxy, random entry with same holding constraints, no-trade baseline.

## Metrics

- Net return, max drawdown, recovery time, profit factor, win rate, average R, trade count, exposure, turnover.

## Kill Criteria

- Performance disappears after costs and spread stress.
- Drawdown exceeds 15% at conservative sizing.
- Results depend on one symbol or narrow parameter set.
- Trade count is too low for inference.

## QA Checklist

- No lookahead from higher timeframe bar alignment.
- Higher timeframe signals use only completed bars.
- Costs and slippage applied.
- Symbol suffixes discovered, not hardcoded.
- Results reproducible from local MT5 data pull.

## Risk Review Questions

- Does trend clustering create correlated losses across USD pairs?
- How much exposure stacks during broad USD moves?
- What is the worst losing streak during range regimes?

## Critic Review Questions

- Is this just a moving average strategy with fragile parameters?
- Does it survive alternate EMA lengths and ATR settings?
- Does it fail in range-bound years?
