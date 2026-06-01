import pandas as pd

from omega01.features.technical import add_atr, add_ema, slope_direction
from omega01.strategies.fx001 import (
    SpreadFilter,
    TrendState,
    align_trends,
    build_trend_state,
    confirm_pullback_resume,
    detect_ema_pullback,
    evaluate_fx001_signal,
    generate_exit_levels,
    is_entry_allowed,
)


def test_add_ema_adds_expected_exponential_average_column() -> None:
    frame = pd.DataFrame({"close": [1.0, 2.0, 3.0]})

    result = add_ema(frame, column="close", period=2, output="ema_2")

    assert list(result["ema_2"].round(6)) == [1.0, 1.666667, 2.555556]


def test_add_atr_uses_true_range_rolling_mean() -> None:
    frame = pd.DataFrame(
        {
            "high": [10.0, 12.0, 13.0],
            "low": [9.0, 10.0, 11.0],
            "close": [9.5, 11.0, 12.0],
        }
    )

    result = add_atr(frame, period=2, output="atr_2")

    assert list(result["atr_2"].round(6)) == [1.0, 1.75, 2.25]


def test_slope_direction_classifies_up_down_and_flat() -> None:
    assert slope_direction(pd.Series([1.0, 2.0, 3.0]), lookback=2, threshold=0.1) == "up"
    assert slope_direction(pd.Series([3.0, 2.0, 1.0]), lookback=2, threshold=0.1) == "down"
    assert slope_direction(pd.Series([1.0, 1.02, 1.03]), lookback=2, threshold=0.1) == "flat"


def test_align_trends_requires_h1_and_h4_same_non_flat_direction() -> None:
    assert align_trends(TrendState("up", True), TrendState("up", True)) == "long"
    assert align_trends(TrendState("down", True), TrendState("down", True)) == "short"
    assert align_trends(TrendState("up", True), TrendState("down", True)) == "none"
    assert align_trends(TrendState("flat", True), TrendState("flat", True)) == "none"


def test_build_trend_state_uses_ema_slope_and_price_side() -> None:
    frame = pd.DataFrame(
        {
            "close": [1.0, 1.1, 1.2, 1.3],
            "ema_3": [0.9, 1.0, 1.1, 1.2],
        }
    )

    state = build_trend_state(frame, ema_column="ema_3", slope_lookback=2, slope_threshold=0.01)

    assert state == TrendState(direction="up", price_on_trend_side=True)


def test_entry_allowed_blocks_high_spread_and_gap_context() -> None:
    spread_filter = SpreadFilter(max_spread=10)

    assert is_entry_allowed(spread=8, spread_filter=spread_filter, has_recent_gap=False)
    assert not is_entry_allowed(spread=11, spread_filter=spread_filter, has_recent_gap=False)
    assert not is_entry_allowed(spread=8, spread_filter=spread_filter, has_recent_gap=True)


def test_detect_ema_pullback_for_long_setup() -> None:
    frame = pd.DataFrame(
        {
            "low": [1.20, 1.18, 1.16],
            "high": [1.24, 1.22, 1.21],
            "close": [1.23, 1.21, 1.19],
            "ema_20": [1.17, 1.17, 1.17],
            "atr_14": [0.02, 0.02, 0.02],
        }
    )

    assert detect_ema_pullback(
        frame,
        direction="long",
        ema_column="ema_20",
        atr_column="atr_14",
        atr_buffer=0.5,
        lookback=3,
    )


def test_detect_ema_pullback_for_short_setup() -> None:
    frame = pd.DataFrame(
        {
            "low": [1.10, 1.11, 1.12],
            "high": [1.14, 1.16, 1.18],
            "close": [1.11, 1.13, 1.15],
            "ema_20": [1.17, 1.17, 1.17],
            "atr_14": [0.02, 0.02, 0.02],
        }
    )

    assert detect_ema_pullback(
        frame,
        direction="short",
        ema_column="ema_20",
        atr_column="atr_14",
        atr_buffer=0.5,
        lookback=3,
    )


def test_detect_ema_pullback_rejects_price_too_far_from_zone() -> None:
    frame = pd.DataFrame(
        {
            "low": [1.30, 1.31, 1.32],
            "high": [1.34, 1.35, 1.36],
            "close": [1.33, 1.34, 1.35],
            "ema_20": [1.17, 1.17, 1.17],
            "atr_14": [0.02, 0.02, 0.02],
        }
    )

    assert not detect_ema_pullback(
        frame,
        direction="long",
        ema_column="ema_20",
        atr_column="atr_14",
        atr_buffer=0.5,
        lookback=3,
    )


def test_confirm_pullback_resume_accepts_long_close_above_prior_high() -> None:
    frame = pd.DataFrame(
        {
            "high": [1.20, 1.21, 1.22],
            "low": [1.17, 1.18, 1.19],
            "close": [1.19, 1.20, 1.225],
        }
    )

    assert confirm_pullback_resume(frame, direction="long")


def test_confirm_pullback_resume_accepts_short_close_below_prior_low() -> None:
    frame = pd.DataFrame(
        {
            "high": [1.24, 1.23, 1.22],
            "low": [1.20, 1.19, 1.18],
            "close": [1.21, 1.20, 1.175],
        }
    )

    assert confirm_pullback_resume(frame, direction="short")


def test_confirm_pullback_resume_rejects_unconfirmed_close() -> None:
    frame = pd.DataFrame(
        {
            "high": [1.20, 1.21, 1.22],
            "low": [1.17, 1.18, 1.19],
            "close": [1.19, 1.20, 1.205],
        }
    )

    assert not confirm_pullback_resume(frame, direction="long")


def test_evaluate_fx001_signal_returns_long_when_all_filters_pass() -> None:
    entry = pd.DataFrame(
        {
            "low": [1.20, 1.18, 1.16, 1.18],
            "high": [1.24, 1.22, 1.21, 1.215],
            "close": [1.23, 1.21, 1.19, 1.225],
            "ema_20": [1.17, 1.17, 1.17, 1.17],
            "atr_14": [0.02, 0.02, 0.02, 0.02],
        }
    )

    signal = evaluate_fx001_signal(
        entry_frame=entry,
        h1=TrendState("up", True),
        h4=TrendState("up", True),
        spread=8,
        spread_filter=SpreadFilter(max_spread=10),
        has_recent_gap=False,
    )

    assert signal == "long"


def test_evaluate_fx001_signal_returns_none_when_trends_conflict() -> None:
    entry = pd.DataFrame(
        {
            "low": [1.20, 1.18, 1.16, 1.18],
            "high": [1.24, 1.22, 1.21, 1.215],
            "close": [1.23, 1.21, 1.19, 1.225],
            "ema_20": [1.17, 1.17, 1.17, 1.17],
            "atr_14": [0.02, 0.02, 0.02, 0.02],
        }
    )

    signal = evaluate_fx001_signal(
        entry_frame=entry,
        h1=TrendState("up", True),
        h4=TrendState("down", True),
        spread=8,
        spread_filter=SpreadFilter(max_spread=10),
        has_recent_gap=False,
    )

    assert signal == "none"


def test_generate_exit_levels_for_long_uses_swing_low_and_atr_target() -> None:
    frame = pd.DataFrame(
        {
            "low": [1.20, 1.18, 1.16],
            "high": [1.24, 1.22, 1.21],
            "close": [1.23, 1.21, 1.19],
            "atr_14": [0.02, 0.02, 0.02],
        }
    )

    levels = generate_exit_levels(
        frame,
        direction="long",
        entry_price=1.22,
        atr_column="atr_14",
        swing_lookback=3,
        atr_stop_multiple=1.5,
        reward_risk=2.0,
    )

    assert levels.stop_loss == 1.16
    assert levels.take_profit == 1.34
    assert levels.risk_per_unit == 0.06


def test_generate_exit_levels_for_short_uses_swing_high_and_atr_target() -> None:
    frame = pd.DataFrame(
        {
            "low": [1.20, 1.18, 1.16],
            "high": [1.24, 1.25, 1.26],
            "close": [1.21, 1.20, 1.19],
            "atr_14": [0.02, 0.02, 0.02],
        }
    )

    levels = generate_exit_levels(
        frame,
        direction="short",
        entry_price=1.20,
        atr_column="atr_14",
        swing_lookback=3,
        atr_stop_multiple=1.5,
        reward_risk=2.0,
    )

    assert levels.stop_loss == 1.26
    assert levels.take_profit == 1.08
    assert levels.risk_per_unit == 0.06


def test_generate_exit_levels_uses_atr_when_swing_is_tighter() -> None:
    frame = pd.DataFrame(
        {
            "low": [1.205, 1.206, 1.207],
            "high": [1.24, 1.22, 1.21],
            "close": [1.23, 1.21, 1.19],
            "atr_14": [0.02, 0.02, 0.02],
        }
    )

    levels = generate_exit_levels(
        frame,
        direction="long",
        entry_price=1.22,
        atr_column="atr_14",
        swing_lookback=3,
        atr_stop_multiple=1.5,
        reward_risk=2.0,
    )

    assert levels.stop_loss == 1.19
    assert levels.take_profit == 1.28
