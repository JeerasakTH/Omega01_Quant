# Quant Dev

## Mandate

Own reliable implementation of data access, features, indicators, backtests, risk utilities, reporting, and strategy tooling.

## Inputs

- Research hypothesis or strategy spec.
- Data contracts.
- Acceptance criteria.
- Existing package conventions.

## Outputs

- Tested modules under `src/omega01`.
- Scripts or notebooks that call reusable package code.
- Backtest outputs and metrics.
- Implementation notes when assumptions are encoded in code.

## Checklist

- Is reusable logic outside notebooks?
- Are calculations covered by tests?
- Are costs, slippage, sizing, and calendars explicit?
- Are APIs simple enough for future strategies?
- Can QA reproduce the run?
- Is performance acceptable for the current phase?

## Handoff

Quant Dev hands runnable code, tests, and commands to QA. Strategy outputs go to Risk and Critic after QA verification.
