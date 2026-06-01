import pandas as pd

from omega01.data.quality import (
    DataQualityReport,
    audit_ohlcv_gaps,
    check_ohlcv_quality,
    find_unexpected_time_gaps,
    is_forex_market_open,
    timeframe_to_timedelta,
)


def test_timeframe_to_timedelta_supports_research_timeframes() -> None:
    assert timeframe_to_timedelta("M5") == pd.Timedelta(minutes=5)
    assert timeframe_to_timedelta("M15") == pd.Timedelta(minutes=15)
    assert timeframe_to_timedelta("H1") == pd.Timedelta(hours=1)
    assert timeframe_to_timedelta("H4") == pd.Timedelta(hours=4)
    assert timeframe_to_timedelta("D1") == pd.Timedelta(days=1)


def test_check_ohlcv_quality_detects_duplicates_missing_values_and_invalid_ohlc() -> None:
    frame = pd.DataFrame(
        {
            "time": [
                "2026-01-05T00:00:00Z",
                "2026-01-05T00:05:00Z",
                "2026-01-05T00:05:00Z",
                "2026-01-05T00:15:00Z",
            ],
            "open": [1.0, 1.1, 1.1, None],
            "high": [1.2, 1.2, 1.0, 1.3],
            "low": [0.9, 1.0, 1.05, 1.1],
            "close": [1.1, 1.15, 1.08, 1.2],
            "tick_volume": [100, 110, 120, 130],
        }
    )

    report = check_ohlcv_quality(frame, symbol="EURUSDm", timeframe="M5")

    assert isinstance(report, DataQualityReport)
    assert report.symbol == "EURUSDm"
    assert report.timeframe == "M5"
    assert report.rows == 4
    assert report.duplicate_timestamps == 1
    assert report.missing_ohlc_rows == 1
    assert report.invalid_ohlc_rows == 1
    assert report.gaps == 1
    assert not report.passed


def test_check_ohlcv_quality_passes_clean_data() -> None:
    frame = pd.DataFrame(
        {
            "time": pd.date_range("2026-01-01", periods=3, freq="5min", tz="UTC"),
            "open": [1.0, 1.1, 1.2],
            "high": [1.2, 1.3, 1.4],
            "low": [0.9, 1.0, 1.1],
            "close": [1.1, 1.2, 1.3],
            "tick_volume": [100, 110, 120],
        }
    )

    report = check_ohlcv_quality(frame, symbol="EURUSDm", timeframe="M5")

    assert report.gaps == 0
    assert report.duplicate_timestamps == 0
    assert report.missing_ohlc_rows == 0
    assert report.invalid_ohlc_rows == 0
    assert report.passed


def test_is_forex_market_open_handles_weekend_closure() -> None:
    assert is_forex_market_open(pd.Timestamp("2026-01-02T20:55:00Z"))
    assert not is_forex_market_open(pd.Timestamp("2026-01-02T21:00:00Z"))
    assert not is_forex_market_open(pd.Timestamp("2026-01-04T21:55:00Z"))
    assert is_forex_market_open(pd.Timestamp("2026-01-04T22:00:00Z"))
    assert not is_forex_market_open(pd.Timestamp("2026-06-07T20:55:00Z"))
    assert is_forex_market_open(pd.Timestamp("2026-06-07T21:00:00Z"))


def test_is_forex_market_open_handles_common_year_end_holiday_closures() -> None:
    assert not is_forex_market_open(pd.Timestamp("2025-12-24T21:00:00Z"))
    assert not is_forex_market_open(pd.Timestamp("2025-12-25T12:00:00Z"))
    assert is_forex_market_open(pd.Timestamp("2025-12-25T22:00:00Z"))
    assert not is_forex_market_open(pd.Timestamp("2025-12-31T21:00:00Z"))
    assert not is_forex_market_open(pd.Timestamp("2026-01-01T12:00:00Z"))
    assert is_forex_market_open(pd.Timestamp("2026-01-01T22:00:00Z"))


def test_check_ohlcv_quality_ignores_expected_forex_weekend_gaps() -> None:
    frame = pd.DataFrame(
        {
            "time": [
                "2026-01-02T20:55:00Z",
                "2026-01-04T22:00:00Z",
                "2026-01-04T22:05:00Z",
            ],
            "open": [1.0, 1.1, 1.2],
            "high": [1.2, 1.3, 1.4],
            "low": [0.9, 1.0, 1.1],
            "close": [1.1, 1.2, 1.3],
            "tick_volume": [100, 110, 120],
        }
    )

    report = check_ohlcv_quality(frame, symbol="EURUSDm", timeframe="M5")

    assert report.gaps == 0
    assert report.passed


def test_check_ohlcv_quality_counts_intraweek_missing_bars() -> None:
    frame = pd.DataFrame(
        {
            "time": [
                "2026-01-05T00:00:00Z",
                "2026-01-05T00:10:00Z",
            ],
            "open": [1.0, 1.1],
            "high": [1.2, 1.3],
            "low": [0.9, 1.0],
            "close": [1.1, 1.2],
            "tick_volume": [100, 110],
        }
    )

    report = check_ohlcv_quality(frame, symbol="EURUSDm", timeframe="M5")

    assert report.gaps == 1
    assert not report.passed


def test_find_unexpected_time_gaps_returns_missing_interval_details() -> None:
    times = pd.Series(
        pd.to_datetime(
            [
                "2026-01-05T00:00:00Z",
                "2026-01-05T00:15:00Z",
                "2026-01-05T00:20:00Z",
            ],
            utc=True,
        )
    )

    gaps = find_unexpected_time_gaps(times, pd.Timedelta(minutes=5))

    assert len(gaps) == 1
    assert gaps[0]["previous_time"] == "2026-01-05T00:00:00+00:00"
    assert gaps[0]["next_time"] == "2026-01-05T00:15:00+00:00"
    assert gaps[0]["missing_open_bars"] == 2


def test_audit_ohlcv_gaps_adds_symbol_and_timeframe() -> None:
    frame = pd.DataFrame(
        {
            "time": [
                "2026-01-05T00:00:00Z",
                "2026-01-05T00:15:00Z",
            ],
            "open": [1.0, 1.1],
            "high": [1.2, 1.3],
            "low": [0.9, 1.0],
            "close": [1.1, 1.2],
        }
    )

    gaps = audit_ohlcv_gaps(frame, symbol="EURUSDm", timeframe="M5")

    assert gaps == [
        {
            "symbol": "EURUSDm",
            "timeframe": "M5",
            "previous_time": "2026-01-05T00:00:00+00:00",
            "next_time": "2026-01-05T00:15:00+00:00",
            "missing_open_bars": 2,
        }
    ]
