from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


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
    gaps = int((unique_times.diff().dropna() > expected_delta).sum())

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
