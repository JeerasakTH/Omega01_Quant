import pandas as pd

from omega01.features.technical import add_atr, add_ema, slope_direction
from omega01.strategies.fx001 import (
    SpreadFilter,
    TrendState,
    align_trends,
    build_trend_state,
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
