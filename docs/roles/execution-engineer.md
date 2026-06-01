# Execution Engineer

## Mandate

Own order simulation, broker integration, fill assumptions, paper trading plumbing, and operational behavior.

## Inputs

- Candidate strategy rules.
- Broker constraints.
- Risk limits.
- Expected order types and trading sessions.

## Outputs

- Execution simulator or adapter.
- Fill and slippage assumptions.
- Paper trading run logs.
- Reconciliation reports.
- Operational incident checklist.

## Checklist

- What order types are supported?
- How are partial fills handled?
- What happens on disconnects, rejected orders, or stale data?
- Are spreads, commissions, and latency measured or estimated?
- Can paper fills be reconciled against expected fills?
- Is there a safe stop procedure?

## Handoff

Execution Engineer hands operational evidence to QA, Risk, and PM before any live-capital decision.
