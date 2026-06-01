# Omega01 Roadmap

This roadmap keeps Omega01 focused on building a research lab before chasing strategy complexity.

## Phase 0: Foundation

Status: in progress

Goal: make the project reproducible, version-controlled, and role-driven.

Deliverables:

- Git repository connected to GitHub.
- Project operating guide in `AGENTS.md`.
- Role charters in `docs/roles/`.
- Basic Python package skeleton.
- Test and lint commands documented.

Exit criteria:

- A new task can name its primary role, expected artifact, and verification method.
- Local tests run from a clean checkout.
- Raw data, generated reports, and secrets are excluded from git.

## Phase 1: Research Operating System

Goal: make every experiment traceable.

Deliverables:

- Strategy spec template.
- Experiment log template.
- Backtest report template.
- Risk review checklist.
- Critic review checklist.
- Naming convention for datasets, experiments, and reports.

Exit criteria:

- Every serious idea has a written hypothesis before coding.
- Every backtest records costs, slippage, validation window, and known limitations.
- Research outputs can be reproduced from committed code plus documented local data inputs.

## Phase 2: Data Layer

Goal: create reliable market data ingestion and validation.

Deliverables:

- Data source inventory.
- Data schema for bars, ticks, symbols, sessions, and corporate actions where relevant.
- Data quality checks for missing values, duplicates, gaps, timezone consistency, and outliers.
- Local storage convention under `data/`.
- Small sample fixtures committed under `tests/fixtures/` when needed.

Exit criteria:

- Data Engineer can ingest a dataset and produce a validation report.
- Quant Dev can consume cleaned data through a stable API.
- QA can reproduce data quality checks without hidden manual steps.

## Phase 3: Backtest Core

Goal: build a minimal but trustworthy backtesting engine.

Deliverables:

- Event or vectorized backtest interface.
- Position sizing module.
- Transaction cost and slippage models.
- Portfolio equity curve and trade ledger outputs.
- Metrics module for returns, drawdown, volatility, Sharpe-like ratios, exposure, turnover, and hit rate.
- Regression tests against simple known strategies.

Exit criteria:

- A simple strategy can run end-to-end from data to report.
- Metrics are tested against deterministic fixtures.
- Risk can inspect drawdowns, exposure, leverage, and concentration.

## Phase 4: First Strategy Research Cycle

Goal: move one strategy from hypothesis to reviewed candidate.

Deliverables:

- Strategy spec in `strategies/`.
- Notebook exploration.
- Promoted reusable feature/backtest code.
- Backtest report in `reports/` or documented generated location.
- QA verification summary.
- Risk review memo.
- Critic memo with limitations and kill criteria.

Exit criteria:

- PM can decide continue, revise, or kill.
- Research conclusions include both positive and negative evidence.
- The implementation is reproducible and covered by targeted tests.

## Phase 5: Portfolio and Risk Layer

Goal: evaluate strategies as portfolio components, not isolated toys.

Deliverables:

- Portfolio allocation assumptions.
- Correlation and overlap analysis.
- Capital usage and leverage constraints.
- Portfolio drawdown and stress scenario reports.
- Risk limits suitable for paper/live sandbox.

Exit criteria:

- Candidate strategies are evaluated together.
- Risk can reject strategies that look good alone but damage portfolio behavior.
- PM has clear capital allocation decision criteria.

## Phase 6: Paper Trading Sandbox

Goal: test operational assumptions without risking capital.

Deliverables:

- Broker or simulated execution adapter.
- Paper trading run log.
- Reconciliation between expected and actual fills.
- Monitoring checklist.
- Incident and rollback procedure.

Exit criteria:

- Execution assumptions are measured, not guessed.
- Failures are visible and recoverable.
- No strategy can reach live capital without QA, Risk, and Critic sign-off.

## Backlog Themes

- Experiment registry.
- Data vendor comparison.
- Regime detection.
- Walk-forward validation.
- Robustness testing and parameter sensitivity.
- Strategy ensemble and allocation.
- Execution simulation.
- Report automation.
- Secrets management and security checklist.
