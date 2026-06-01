from __future__ import annotations

import pandas as pd


def add_ema(
    frame: pd.DataFrame,
    column: str = "close",
    period: int = 20,
    output: str | None = None,
) -> pd.DataFrame:
    result = frame.copy()
    output_column = output or f"ema_{period}"
    result[output_column] = result[column].ewm(span=period, adjust=False).mean()
    return result


def add_atr(frame: pd.DataFrame, period: int = 14, output: str | None = None) -> pd.DataFrame:
    result = frame.copy()
    output_column = output or f"atr_{period}"
    previous_close = result["close"].shift(1)
    true_range = pd.concat(
        [
            result["high"] - result["low"],
            (result["high"] - previous_close).abs(),
            (result["low"] - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    result[output_column] = true_range.rolling(window=period, min_periods=1).mean()
    return result


def slope_direction(series: pd.Series, lookback: int = 3, threshold: float = 0.0) -> str:
    if len(series) <= lookback:
        return "flat"
    slope = float(series.iloc[-1] - series.iloc[-1 - lookback])
    if slope > threshold:
        return "up"
    if slope < -threshold:
        return "down"
    return "flat"
