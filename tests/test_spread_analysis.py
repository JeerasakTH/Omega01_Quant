import pandas as pd

from omega01.data.spread import SpreadReport, analyze_spread, recommend_max_spread


def test_analyze_spread_summarizes_distribution() -> None:
    frame = pd.DataFrame({"spread": [10, 12, 12, 20, 100]})

    report = analyze_spread(frame, symbol="EURUSDm", timeframe="M5")

    assert isinstance(report, SpreadReport)
    assert report.symbol == "EURUSDm"
    assert report.timeframe == "M5"
    assert report.rows == 5
    assert report.median == 12.0
    assert report.p90 == 68.0
    assert report.p95 == 84.0
    assert report.max_spread == 100


def test_recommend_max_spread_uses_p95_with_minimum_buffer() -> None:
    report = SpreadReport(
        symbol="EURUSDm",
        timeframe="M5",
        rows=100,
        median=12.0,
        p75=14.0,
        p90=20.0,
        p95=22.0,
        p99=30.0,
        max_spread=100,
        zero_spread_rows=0,
    )

    assert recommend_max_spread(report) == 22


def test_recommend_max_spread_never_below_median_plus_buffer() -> None:
    report = SpreadReport(
        symbol="EURUSDm",
        timeframe="M5",
        rows=100,
        median=10.0,
        p75=10.0,
        p90=10.0,
        p95=10.0,
        p99=11.0,
        max_spread=12,
        zero_spread_rows=0,
    )

    assert recommend_max_spread(report, minimum_buffer=3) == 13
