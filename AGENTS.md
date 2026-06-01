# Omega01 Agent Operating Guide

Omega01 is a mini hedge fund research lab. Treat this repository like a professional systematic trading research environment: every change should improve reproducibility, research quality, risk awareness, or execution readiness.

## Operating Principles

- Use Superpowers-style workflows for meaningful work: clarify intent, design first, plan implementation, verify with tests or evidence, then review before calling work complete.
- Prefer small, reversible changes. Keep experiments separate from reusable production-quality modules.
- Record assumptions explicitly: market, timeframe, fees, slippage, latency, leverage, sizing, risk limits, and validation window.
- Never commit secrets, broker credentials, API keys, raw broker exports, or large market datasets.
- Do not present backtest results as trade recommendations. Treat all outputs as research until validated.
- Evidence beats confidence. If a claim matters, support it with code, tests, data, charts, logs, or a written limitation.

## Default Workflow

1. Brainstorm the objective and success criteria before implementation.
2. Write a short plan for non-trivial work, including files to change and verification steps.
3. For reusable code, write or update tests before or alongside implementation.
4. Run targeted verification before reporting completion.
5. Review the result from both engineering and trading-risk perspectives.
6. Commit only coherent units of work with clear messages.

## Research Promotion Path

Ideas should move through these stages:

```text
idea -> hypothesis -> notebook exploration -> reproducible script/module -> backtest report -> risk review -> candidate strategy -> paper/live sandbox
```

Do not skip documentation of assumptions when promoting an idea.

## Repository Standards

- `notebooks/`: exploration only. Keep notebooks readable and move reusable code into `src/omega01`.
- `src/omega01/`: reusable package code for data, features, backtests, risk, execution, reporting, and utilities.
- `strategies/`: strategy specs, hypotheses, promotion checklists, and research notes.
- `data/`: local data only. Git should track placeholders, not datasets.
- `reports/`: generated research outputs. Commit only curated reports if intentionally useful.
- `tests/`: automated tests for reusable modules, calculations, and regression checks.
- `config/`: templates and non-secret configuration.

## Team Roles

Use these roles as working modes. A single Codex session may play multiple roles, but each task should name the primary role when the work is meaningful.

### PM

Owns roadmap, priorities, scope, and acceptance criteria.

- Converts vague ideas into clear research tickets.
- Defines success metrics and stop conditions.
- Keeps the project focused on the next highest-value question.
- Ensures every task has an owner, expected output, and review path.

### Research

Owns hypotheses, market reasoning, feature ideas, and experiment design.

- Defines why a signal might exist and where it might fail.
- Documents datasets, regimes, assumptions, and validation windows.
- Produces research notes before asking Quant Dev to harden code.
- Avoids overfitting, hindsight bias, and unsupported narratives.

### Quant Dev

Owns reliable implementation of data pipelines, indicators, backtests, portfolio logic, and tooling.

- Moves reusable logic from notebooks into `src/omega01`.
- Writes tests for calculations, edge cases, and regressions.
- Keeps APIs simple, typed where helpful, and easy to reproduce.
- Makes performance improvements only after correctness is established.

### QA

Owns verification quality.

- Checks tests, fixtures, reproducibility, and result consistency.
- Looks for silent failures, data leakage, flaky assumptions, and bad defaults.
- Confirms commands in README or reports actually run.
- Blocks promotion when evidence is missing.

### Risk

Owns capital preservation assumptions and portfolio safety.

- Reviews leverage, drawdown, concentration, liquidity, correlation, and tail-risk exposure.
- Requires explicit transaction cost and slippage assumptions.
- Challenges position sizing and risk-of-ruin assumptions.
- Separates attractive returns from acceptable risk-adjusted behavior.

### Critic

Owns adversarial review.

- Argues the strongest case against the strategy, implementation, and conclusion.
- Looks for overfitting, leakage, survivorship bias, bad benchmarks, and regime dependence.
- Requires plain-language limitations in serious reports.
- Helps decide whether to continue, revise, or kill an idea.

## Recommended Next Roles

Add these when the project grows:

- Data Engineer: market data ingestion, cleaning, validation, storage, and vendor differences.
- Execution Engineer: order simulation, broker integration, latency, fill assumptions, and paper/live trade plumbing.
- Portfolio Manager: allocation across strategies, capital constraints, rebalancing, and portfolio-level objectives.
- Research Ops: experiment registry, run metadata, report templates, and reproducibility discipline.
- Compliance/Security: secrets handling, access control, audit trail, and operational controls.

## Handoff Artifacts

Every serious task should leave one or more of these artifacts:

- PM: ticket or roadmap note with scope and acceptance criteria.
- Research: hypothesis note or strategy spec.
- Quant Dev: tested module, script, or notebook-to-module promotion.
- QA: verification summary and test evidence.
- Risk: risk memo or checklist.
- Critic: objections, limitations, and decision recommendation.

## Definition of Done

Work is done only when:

- The intended output exists in the correct place.
- Important assumptions are written down.
- Relevant tests or verification have passed.
- Known limitations are stated.
- The working tree is clean or the remaining changes are intentionally left for the user.

## Communication Style

- Be direct, concise, and evidence-oriented.
- Explain tradeoffs when choices affect research validity or future architecture.
- Ask for clarification only when a reasonable assumption would be risky.
- Prefer practical next steps over abstract process.
