from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


FOREX_WEEK_OPEN_HOUR_UTC = 21
FOREX_WEEK_CLOSE_HOUR_UTC = 21


@dataclass(frozen=True)
class DataQualityReport:
    symbol: str
    timeframe: str
    rows: int
    first_time: str
    last_time: str
    duplicate_timestamps: int
    missing_ohlc_rows: int
    invalid_ohlc_rows: int
    gaps: int
    passed: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def timeframe_to_timedelta(timeframe: str) -> pd.Timedelta:
    normalized = timeframe.upper()
    if normalized.startswith("M"):
        return pd.Timedelta(minutes=int(normalized[1:]))
    if normalized.startswith("H"):
        return pd.Timedelta(hours=int(normalized[1:]))
    if normalized == "D1":
        return pd.Timedelta(days=1)
    raise ValueError(f"Unsupported timeframe: {timeframe}")


def is_forex_market_open(timestamp: pd.Timestamp) -> bool:
    ts = pd.Timestamp(timestamp)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    ts = ts.tz_convert("UTC")

    weekday = ts.weekday()
    hour = ts.hour
    month_day = (ts.month, ts.day)
    if month_day in {(12, 24), (12, 31)} and hour >= FOREX_WEEK_CLOSE_HOUR_UTC:
        return False
    if month_day in {(12, 25), (1, 1)}:
        return hour >= 22

    if weekday < 4:
        return True
    if weekday == 4:
        return hour < FOREX_WEEK_CLOSE_HOUR_UTC
    if weekday == 5:
        return False
    return hour >= forex_week_open_hour_utc(ts)


def forex_week_open_hour_utc(timestamp: pd.Timestamp) -> int:
    ts = pd.Timestamp(timestamp)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    ts = ts.tz_convert("UTC")
    if ts.month in {11, 12, 1, 2}:
        return 22
    return FOREX_WEEK_OPEN_HOUR_UTC


def find_unexpected_time_gaps(
    times: pd.Series, expected_delta: pd.Timedelta
) -> list[dict[str, object]]:
    gaps: list[dict[str, object]] = []
    unique_times = times.drop_duplicates().sort_values()
    for previous, current in zip(unique_times.iloc[:-1], unique_times.iloc[1:]):
        expected = previous + expected_delta
        missing_open_bars = 0
        while expected < current:
            if is_forex_market_open(expected):
                missing_open_bars += 1
            expected += expected_delta
        if missing_open_bars:
            gaps.append(
                {
                    "previous_time": previous.isoformat(),
                    "next_time": current.isoformat(),
                    "missing_open_bars": missing_open_bars,
                }
            )
    return gaps


def count_unexpected_time_gaps(times: pd.Series, expected_delta: pd.Timedelta) -> int:
    return len(find_unexpected_time_gaps(times, expected_delta))


def audit_ohlcv_gaps(
    frame: pd.DataFrame, symbol: str, timeframe: str
) -> list[dict[str, object]]:
    if frame.empty:
        return []

    data = frame.copy()
    data["time"] = pd.to_datetime(data["time"], utc=True)
    gaps = find_unexpected_time_gaps(
        data["time"],
        timeframe_to_timedelta(timeframe),
    )
    return [
        {
            "symbol": symbol,
            "timeframe": timeframe,
            **gap,
        }
        for gap in gaps
    ]


def check_ohlcv_quality(frame: pd.DataFrame, symbol: str, timeframe: str) -> DataQualityReport:
    if frame.empty:
        return DataQualityReport(
            symbol=symbol,
            timeframe=timeframe,
            rows=0,
            first_time="",
            last_time="",
            duplicate_timestamps=0,
            missing_ohlc_rows=0,
            invalid_ohlc_rows=0,
            gaps=0,
            passed=False,
        )

    data = frame.copy()
    data["time"] = pd.to_datetime(data["time"], utc=True)
    data = data.sort_values("time")

    ohlc_columns = ["open", "high", "low", "close"]
    duplicate_timestamps = int(data["time"].duplicated().sum())
    missing_ohlc_rows = int(data[ohlc_columns].isna().any(axis=1).sum())
    invalid_ohlc_rows = int(
        (
            (data["high"] < data[["open", "close"]].max(axis=1))
            | (data["low"] > data[["open", "close"]].min(axis=1))
            | (data["high"] < data["low"])
        ).sum()
    )

    unique_times = data["time"].drop_duplicates().sort_values()
    expected_delta = timeframe_to_timedelta(timeframe)
    gaps = count_unexpected_time_gaps(unique_times, expected_delta)

    passed = duplicate_timestamps == 0 and missing_ohlc_rows == 0 and invalid_ohlc_rows == 0 and gaps == 0
    return DataQualityReport(
        symbol=symbol,
        timeframe=timeframe,
        rows=len(data),
        first_time=unique_times.iloc[0].isoformat(),
        last_time=unique_times.iloc[-1].isoformat(),
        duplicate_timestamps=duplicate_timestamps,
        missing_ohlc_rows=missing_ohlc_rows,
        invalid_ohlc_rows=invalid_ohlc_rows,
        gaps=gaps,
        passed=passed,
    )
