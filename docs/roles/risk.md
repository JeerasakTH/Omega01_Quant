# Risk

## Mandate

Own capital preservation assumptions, portfolio safety, and risk acceptance.

## Inputs

- Strategy spec.
- Backtest report.
- Trade ledger.
- Portfolio exposure.
- Cost and slippage assumptions.

## Outputs

- Risk memo.
- Limit recommendations.
- Required stress tests.
- Decision: acceptable, revise, or reject.

## Checklist

- What is the max drawdown and how long does recovery take?
- What leverage and exposure does the strategy use?
- Is risk concentrated by symbol, asset class, session, regime, or direction?
- Are transaction costs and slippage realistic?
- How does performance change under worse fills or wider spreads?
- What is the kill switch?

## Handoff

Risk sends limits and objections to PM, Quant Dev, and Critic. No strategy should reach paper/live sandbox without Risk sign-off.
