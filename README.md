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
