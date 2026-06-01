from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from omega01.features.technical import slope_direction


@dataclass(frozen=True)
class TrendState:
    direction: str
    price_on_trend_side: bool


@dataclass(frozen=True)
class SpreadFilter:
    max_spread: int


def align_trends(h1: TrendState, h4: TrendState) -> str:
    if not h1.price_on_trend_side or not h4.price_on_trend_side:
        return "none"
    if h1.direction == h4.direction == "up":
        return "long"
    if h1.direction == h4.direction == "down":
        return "short"
    return "none"


def build_trend_state(
    frame: pd.DataFrame,
    ema_column: str,
    slope_lookback: int,
    slope_threshold: float,
) -> TrendState:
    direction = slope_direction(
        frame[ema_column],
        lookback=slope_lookback,
        threshold=slope_threshold,
    )
    latest_close = float(frame["close"].iloc[-1])
    latest_ema = float(frame[ema_column].iloc[-1])
    if direction == "up":
        price_on_trend_side = latest_close >= latest_ema
    elif direction == "down":
        price_on_trend_side = latest_close <= latest_ema
    else:
        price_on_trend_side = False
    return TrendState(direction=direction, price_on_trend_side=price_on_trend_side)


def is_entry_allowed(spread: int, spread_filter: SpreadFilter, has_recent_gap: bool) -> bool:
    return spread <= spread_filter.max_spread and not has_recent_gap
