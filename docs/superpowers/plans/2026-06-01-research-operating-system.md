# Research Operating System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first Omega01 research operating system for forex strategy research.

**Architecture:** Keep process artifacts in `docs/` and strategy-specific specs in `strategies/forex/`. Templates define the required shape of future research, while the first five specs turn the strategy universe into concrete research tickets.

**Tech Stack:** Markdown documentation, Omega01 role workflow, MT5/Exness forex data assumptions, Python package verification with pytest.

---

### Task 1: Create Research Templates

**Files:**
- Create: `docs/templates/strategy-spec-template.md`
- Create: `docs/templates/experiment-log-template.md`
- Create: `docs/templates/backtest-report-template.md`
- Create: `docs/templates/risk-review-template.md`
- Create: `docs/templates/critic-review-template.md`
- Create: `docs/templates/research-ticket-template.md`
- Create: `docs/templates/decision-log-template.md`

- [x] **Step 1: Add templates with required sections**

Each template must include owner role, inputs, assumptions, evidence, review gates, and decision fields.

- [x] **Step 2: Link templates from README**

Run: `git diff -- README.md docs/templates`

Expected: README points to `docs/templates/`.

### Task 2: Create First Five Strategy Specs

**Files:**
- Create: `strategies/forex/FX-001-mtf-trend-following.md`
- Create: `strategies/forex/FX-002-range-mean-reversion.md`
- Create: `strategies/forex/FX-003-london-breakout.md`
- Create: `strategies/forex/FX-004-atr-volatility-breakout.md`
- Create: `strategies/forex/FX-018-volatility-regime-switcher.md`

- [x] **Step 1: Convert first research basket into specs**

Each spec must include market, timeframe, hypothesis, signal, entry, exit, sizing, risk limits, data requirements, validation plan, kill criteria, QA checks, Risk concerns, and Critic questions.

- [x] **Step 2: Verify no strategy promotes live trading**

Run: `Select-String -Path strategies/forex/*.md -Pattern "research only"`

Expected: all specs clearly remain research-only artifacts.

### Task 3: Update Project Planning Docs

**Files:**
- Modify: `README.md`
- Modify: `docs/roadmap.md`
- Modify: `docs/research/strategy-universe.md`
- Create: `strategies/forex/README.md`

- [x] **Step 1: Link templates and specs**

Add navigation links so future sessions can find the work.

- [x] **Step 2: Mark Phase 1 artifacts as started**

Update roadmap with template/spec deliverables.

### Task 4: Verification

**Files:**
- Read: `tests/test_package.py`

- [ ] **Step 1: Run unit tests**

Run: `.venv\Scripts\python.exe -m pytest`

Expected: `1 passed`

- [ ] **Step 2: Review git status**

Run: `git status --short --branch`

Expected: only intended documentation changes are present.
