# Omega01 Quant

Mini hedge fund research lab for systematic trading ideas, data workflows, backtests, and portfolio research.

## Purpose

- Research trading signals and portfolio rules.
- Build reusable data, backtest, risk, and execution modules.
- Keep experiments reproducible with version-controlled assumptions.
- Separate exploratory work from production-quality research code.

## Repository Layout

```text
config/        Configuration templates and research settings
data/          Local datasets, ignored by git except placeholders
notebooks/     Exploratory notebooks
reports/       Generated charts, tables, and research outputs
src/omega01/   Reusable Python package code
strategies/    Strategy research notes and definitions
tests/         Automated tests
```

## Getting Started

```powershell
cd C:\Quant\Omega01
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

## Research Rules

- Commit code, configs, and written assumptions.
- Do not commit raw market data, broker exports, credentials, or generated reports.
- Record transaction costs, slippage, position sizing, and risk limits for every serious backtest.
- Promote notebook ideas into `src/omega01` once they become reusable.

See `AGENTS.md` for the project operating guide, role definitions, and research workflow.

Project planning lives in `docs/roadmap.md`. Role charters live in `docs/roles/`.

The first forex strategy research universe lives in `docs/research/strategy-universe.md`.
The first MT5/Exness forex inventory summary lives in `docs/research/mt5-forex-inventory.md`.
The first major-pair data quality summary lives in `docs/research/mt5-major-data-quality.md`.
The first MT5 spread analysis lives in `docs/research/mt5-spread-analysis.md`.

Research templates live in `docs/templates/`. First-pass forex strategy specs live in `strategies/forex/`.
