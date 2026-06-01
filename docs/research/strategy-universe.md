# Forex Strategy Research Universe

Primary mode: PM + Research

This document defines the first Omega01 forex strategy universe. It is not a trading recommendation. It is a research map for selecting hypotheses to test using MT5/Exness data before any EA or live deployment.

## Current Mandate

- Market: forex first, with room for gold later if data quality is reliable.
- Platform/data: MT5 with Exness symbols.
- Timeframes: broad scan across M1, M5, M15, M30, H1, H4, and D1. Strategy-specific timeframes are allowed.
- Automation target: research automation first, EA later.
- Risk appetite: portfolio-level maximum drawdown tolerance around 25%, subject to Risk review.
- Research goal: build multiple strategies for different regimes instead of one all-weather strategy.

## Risk Buckets

### Low Risk

Expected behavior:

- Lower trade frequency or stronger filters.
- Smaller leverage and tighter exposure caps.
- Avoids trading during unstable spread/news conditions unless explicitly designed for them.
- Prioritizes robustness over high return.

Initial drawdown expectation:

- Strategy-level research target: ideally under 10-15% before portfolio combination.
- Portfolio contribution: defensive or stabilizing.

### Medium Risk

Expected behavior:

- More active entries.
- Uses volatility, trend, or regime filters.
- Accepts moderate drawdowns for better opportunity capture.

Initial drawdown expectation:

- Strategy-level research target: under 15-25% if returns justify it.
- Portfolio contribution: core return engine.

### High Risk

Expected behavior:

- Trades fast moves, breakouts, event windows, or aggressive mean reversion.
- Requires strict kill switches and position limits.
- Cannot be promoted without strong Risk and Critic review.

Initial drawdown expectation:

- Strategy-level drawdown may approach or exceed 25% in research, but must not dominate portfolio risk.
- Portfolio contribution: small allocation, convex opportunity, or tactical mode only.

## Market Regime Map

| Regime | Description | Useful signals | Avoid |
| --- | --- | --- | --- |
| Trend | Directional persistence across sessions | MA slope, breakout, ADX, higher-high/lower-low structure | fading strong moves too early |
| Range | Price oscillates inside stable bands | z-score, Bollinger bands, RSI, support/resistance | breakout chasing |
| High volatility | Wide ranges, fast repricing, unstable spreads | ATR expansion, session/news filters, volatility breakout | tight stops without spread control |
| Low volatility | Compressed range, quiet session | compression breakout setup, carry/session bias | overtrading noise |
| News/event | Scheduled or unscheduled shocks | calendar windows, spread expansion, momentum burst | assuming historical fills are realistic |
| Mean reversion | Short-term dislocation snaps back | z-score, deviation from VWAP/MA, RSI extremes | averaging down without hard limits |

## Initial Hypothesis List

| ID | Hypothesis | Risk | Regime | Candidate timeframes | Research priority |
| --- | --- | --- | --- | --- | --- |
| FX-001 | Conservative multi-timeframe trend following: trade only when H1/H4 trend agrees and M15/M30 pullback resumes. | Low | Trend | M15, M30, H1, H4 | High |
| FX-002 | Range mean reversion: trade Bollinger/z-score extremes only when ADX and ATR indicate stable range. | Low | Range, mean reversion | M5, M15, M30 | High |
| FX-003 | London session breakout after Asian range compression with strict spread and time stop filters. | Medium | Low volatility to trend | M5, M15, M30 | High |
| FX-004 | ATR volatility breakout: enter when price breaks recent range during volatility expansion, exit by trailing ATR stop. | Medium | High volatility, trend | M5, M15, H1 | High |
| FX-005 | Trend pullback continuation: buy/sell pullbacks to EMA zone only when higher timeframe slope is strong. | Medium | Trend | M5, M15, H1 | High |
| FX-006 | Intraday VWAP/mean reversion proxy using session midpoint or rolling average when price overextends in quiet conditions. | Low | Range, mean reversion | M5, M15 | Medium |
| FX-007 | Breakout failure fade: fade failed highs/lows when price quickly returns inside prior range with volatility cooling. | Medium | Range, high volatility reversal | M5, M15, M30 | Medium |
| FX-008 | Momentum continuation after strong candle close, filtered by spread, ATR, and session liquidity. | Medium | Trend, high volatility | M1, M5, M15 | Medium |
| FX-009 | Daily bias strategy: trade intraday only in direction of D1/H4 bias after first pullback. | Low | Trend | M15, H1, H4, D1 | Medium |
| FX-010 | Low-volatility compression scanner: do not trade compression itself, but prepare breakout orders after defined squeeze. | Medium | Low volatility to high volatility | M5, M15, H1 | Medium |
| FX-011 | Countertrend exhaustion: fade parabolic short-term moves after ATR multiple extension and reversal confirmation. | High | High volatility, mean reversion | M1, M5, M15 | Medium |
| FX-012 | Session reversal: test whether late London or NY close mean reversion exists after one-sided intraday moves. | Medium | Mean reversion, session effect | M5, M15, H1 | Medium |
| FX-013 | Multi-pair USD strength filter: trade only pairs aligned with broad USD basket direction. | Low | Trend | M15, H1, H4 | Medium |
| FX-014 | Pair relative strength rotation: rank major pairs by momentum and trade strongest versus weakest with volatility cap. | Medium | Trend | H1, H4, D1 | Medium |
| FX-015 | Spread-aware scalping prototype: only research during liquid windows with strict max spread and tiny holding time. | High | Low volatility, micro trend | M1, M5 | Low |
| FX-016 | News blackout filter: not a standalone strategy; improves other strategies by skipping high-spread event windows. | Low | News/event risk control | M1-H1 | High as filter |
| FX-017 | Grid recovery research under hard risk caps: test whether any grid-like behavior survives fixed max loss and no martingale escalation. | High | Range | M1, M5, M15 | Low, Risk gated |
| FX-018 | Volatility regime switcher: choose trend, range, or no-trade mode based on ATR percentile and ADX structure. | Medium | Multi-regime | M15, H1, H4 | High as meta-layer |

## First Research Basket

Start with strategies that are diverse, testable, and useful as building blocks.

Recommended first five:

1. [FX-001 Conservative multi-timeframe trend following](../../strategies/forex/FX-001-mtf-trend-following.md).
2. [FX-002 Range mean reversion with regime filter](../../strategies/forex/FX-002-range-mean-reversion.md).
3. [FX-003 London session breakout after Asian range](../../strategies/forex/FX-003-london-breakout.md).
4. [FX-004 ATR volatility breakout](../../strategies/forex/FX-004-atr-volatility-breakout.md).
5. [FX-018 Volatility regime switcher as meta-layer](../../strategies/forex/FX-018-volatility-regime-switcher.md).

Why these first:

- They cover trend, range, volatility expansion, session behavior, and regime selection.
- They can share early data loaders and metrics.
- They are easier to verify than news scalping or grid recovery.
- They support portfolio construction because they should behave differently across regimes.

## Selection Criteria

Score each hypothesis from 1 to 5.

| Criterion | Meaning | Weight |
| --- | --- | --- |
| Clarity | Rules can be expressed without vague discretion. | 20% |
| Data availability | Required data is available from MT5/Exness or can be approximated cleanly. | 15% |
| Risk controllability | Stops, sizing, exposure, and kill criteria are explicit. | 20% |
| Regime usefulness | Strategy fills a clear role in the portfolio. | 15% |
| Robustness potential | Less likely to depend on fragile parameters. | 15% |
| Implementation cost | Can be tested with current project maturity. | 10% |
| Critic survivability | Obvious overfitting/leakage objections are manageable. | 5% |

Initial priority rule:

- Research first if weighted score is at least 3.8 and implementation cost is not the main blocker.
- Put in backlog if score is 3.0-3.7 or it depends on missing infrastructure.
- Reject or quarantine if risk controllability is under 3.

## Default Forex Research Universe

Start with major and liquid symbols available in Exness MT5:

- EURUSD
- GBPUSD
- USDJPY
- USDCHF
- USDCAD
- AUDUSD
- NZDUSD
- EURJPY
- GBPJPY
- XAUUSD only after forex data workflow is stable

Symbol suffixes such as `m` should be discovered from the local MT5 terminal instead of hardcoded.

The first Exness MT5 inventory found 28 forex symbols using the `m` suffix. See `mt5-forex-inventory.md`.

## Timeframe Plan

Use timeframes by role:

- M1: microstructure/scalping research only; high QA burden.
- M5: intraday entries, breakout timing, short mean reversion.
- M15: primary intraday research timeframe.
- M30: smoother intraday confirmation.
- H1: trend, volatility, session structure.
- H4: higher timeframe bias and regime context.
- D1: macro bias, long-term filter, benchmark context.

Initial data pull target:

- M5 and M15 for broad intraday tests.
- H1 and H4 for context filters.
- D1 for bias and benchmark features.

## Risk Guardrails

Default research guardrails before a strategy can be promoted:

- No unlimited averaging down.
- No martingale escalation.
- Every trade has an initial invalidation condition.
- Max spread filter must be part of intraday strategies.
- Position sizing must be explicit and capped.
- Worst-case stop behavior must be modeled.
- Strategy-level DD near 25% requires strong justification and small portfolio allocation.
- News/event strategies require separate execution realism review.

## First Data Questions

Before coding backtests, answer:

- What exact Exness symbol names are available in MT5?
- How much historical data exists for M5, M15, H1, H4, and D1?
- Are spreads available historically, or do we need assumptions?
- Which sessions should be used for London, New York, and Asian range logic?
- What timezone does the MT5 terminal data use?

## Next Actions

1. Create strategy spec templates for the first five hypotheses.
2. Build an MT5 data inventory script that lists symbols and available date ranges by timeframe.
3. Pull sample data for EURUSD, GBPUSD, USDJPY, and XAUUSD candidate symbols.
4. Define shared metrics and drawdown calculation standards.
5. Let Risk and Critic review FX-001 to FX-005 before implementation.
