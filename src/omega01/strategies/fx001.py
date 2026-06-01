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


@dataclass(frozen=True)
class ExitLevels:
    stop_loss: float
    take_profit: float
    risk_per_unit: float


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


def detect_ema_pullback(
    frame: pd.DataFrame,
    direction: str,
    ema_column: str,
    atr_column: str,
    atr_buffer: float,
    lookback: int,
) -> bool:
    recent = frame.tail(lookback)
    if recent.empty:
        return False

    ema = recent[ema_column]
    buffer = recent[atr_column] * atr_buffer
    if direction == "long":
        return bool((recent["low"] <= ema + buffer).any())
    if direction == "short":
        return bool((recent["high"] >= ema - buffer).any())
    return False


def confirm_pullback_resume(frame: pd.DataFrame, direction: str) -> bool:
    if len(frame) < 2:
        return False

    latest = frame.iloc[-1]
    previous = frame.iloc[-2]
    if direction == "long":
        return bool(latest["close"] > previous["high"])
    if direction == "short":
        return bool(latest["close"] < previous["low"])
    return False


def evaluate_fx001_signal(
    entry_frame: pd.DataFrame,
    h1: TrendState,
    h4: TrendState,
    spread: int,
    spread_filter: SpreadFilter,
    has_recent_gap: bool,
    ema_column: str = "ema_20",
    atr_column: str = "atr_14",
    atr_buffer: float = 0.5,
    pullback_lookback: int = 3,
) -> str:
    if not is_entry_allowed(spread, spread_filter, has_recent_gap):
        return "none"

    aligned_direction = align_trends(h1, h4)
    if aligned_direction == "none":
        return "none"

    if not detect_ema_pullback(
        entry_frame,
        direction=aligned_direction,
        ema_column=ema_column,
        atr_column=atr_column,
        atr_buffer=atr_buffer,
        lookback=pullback_lookback,
    ):
        return "none"

    if not confirm_pullback_resume(entry_frame, direction=aligned_direction):
        return "none"

    return aligned_direction


def generate_exit_levels(
    frame: pd.DataFrame,
    direction: str,
    entry_price: float,
    atr_column: str,
    swing_lookback: int,
    atr_stop_multiple: float,
    reward_risk: float,
) -> ExitLevels:
    recent = frame.tail(swing_lookback)
    latest_atr = float(recent[atr_column].iloc[-1])

    if direction == "long":
        swing_stop = float(recent["low"].min())
        atr_stop = entry_price - latest_atr * atr_stop_multiple
        stop_loss = min(swing_stop, atr_stop)
        risk_per_unit = entry_price - stop_loss
        take_profit = entry_price + risk_per_unit * reward_risk
    elif direction == "short":
        swing_stop = float(recent["high"].max())
        atr_stop = entry_price + latest_atr * atr_stop_multiple
        stop_loss = max(swing_stop, atr_stop)
        risk_per_unit = stop_loss - entry_price
        take_profit = entry_price - risk_per_unit * reward_risk
    else:
        raise ValueError(f"Unsupported direction: {direction}")

    return ExitLevels(
        stop_loss=round(stop_loss, 10),
        take_profit=round(take_profit, 10),
        risk_per_unit=round(risk_per_unit, 10),
    )
