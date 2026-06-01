# Strategy Spec Template

## Header

- Strategy ID:
- Name:
- Owner role: Research
- Supporting roles: PM, Quant Dev, QA, Risk, Critic
- Status: draft | research | backtest | review | candidate | killed
- Risk bucket: low | medium | high
- Regime:

## Research-Only Notice

This is a research artifact, not a trade recommendation or live deployment approval.

## Hypothesis

Describe the market behavior this strategy expects to exploit.

## Market and Instruments

- Market:
- Symbols:
- Broker/data source:
- Timezone assumption:

## Timeframes

- Entry timeframe:
- Confirmation timeframe:
- Context timeframe:

## Signals

- Trend/regime filter:
- Entry signal:
- Exit signal:
- No-trade filter:

## Entry Rules

Long:

- 

Short:

- 

## Exit Rules

- Stop loss:
- Take profit:
- Time stop:
- Invalidating condition:

## Position Sizing

- Sizing model:
- Max risk per trade:
- Max simultaneous positions:
- Max symbol exposure:

## Costs and Execution Assumptions

- Spread:
- Commission:
- Slippage:
- Fill model:
- News/event handling:

## Data Requirements

- OHLCV:
- Spread:
- Sessions:
- Minimum history:

## Validation Plan

- In-sample period:
- Out-of-sample period:
- Walk-forward plan:
- Symbols:
- Benchmarks:

## Metrics

- Return:
- Max drawdown:
- Recovery time:
- Sharpe-like ratio:
- Profit factor:
- Win rate:
- Average R:
- Turnover:
- Exposure:

## Kill Criteria

- 

## QA Checklist

- No lookahead.
- No future bar usage.
- Timezone and session logic documented.
- Costs and slippage applied.
- Results reproducible from committed code and documented local data.

## Risk Review Questions

- 

## Critic Review Questions

- 
