import pandas as pd

from omega01.data.quality import DataQualityReport, check_ohlcv_quality, timeframe_to_timedelta


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
                "2026-01-01T00:00:00Z",
                "2026-01-01T00:05:00Z",
                "2026-01-01T00:05:00Z",
                "2026-01-01T00:15:00Z",
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
