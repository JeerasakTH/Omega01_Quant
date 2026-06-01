import pandas as pd

from omega01.data.alignment import align_completed_higher_timeframe


def test_align_completed_higher_timeframe_uses_only_closed_higher_bars() -> None:
    entry = pd.DataFrame(
        {
            "time": pd.to_datetime(
                [
                    "2026-01-05T00:15:00Z",
                    "2026-01-05T00:45:00Z",
                    "2026-01-05T01:00:00Z",
                    "2026-01-05T01:15:00Z",
                ],
                utc=True,
            ),
            "close": [1.0, 1.1, 1.2, 1.3],
        }
    )
    higher = pd.DataFrame(
        {
            "time": pd.to_datetime(
                [
                    "2026-01-05T00:00:00Z",
                    "2026-01-05T01:00:00Z",
                ],
                utc=True,
            ),
            "h1_direction": ["up", "down"],
        }
    )

    aligned = align_completed_higher_timeframe(
        entry,
        higher,
        higher_timeframe="H1",
        columns=["h1_direction"],
    )

    assert pd.isna(aligned.loc[0, "h1_direction"])
    assert pd.isna(aligned.loc[1, "h1_direction"])
    assert aligned.loc[2, "h1_direction"] == "up"
    assert aligned.loc[3, "h1_direction"] == "up"


def test_align_completed_higher_timeframe_prefixes_columns() -> None:
    entry = pd.DataFrame(
        {
            "time": pd.to_datetime(["2026-01-05T04:00:00Z"], utc=True),
            "close": [1.0],
        }
    )
    higher = pd.DataFrame(
        {
            "time": pd.to_datetime(["2026-01-05T00:00:00Z"], utc=True),
            "direction": ["up"],
        }
    )

    aligned = align_completed_higher_timeframe(
        entry,
        higher,
        higher_timeframe="H4",
        columns=["direction"],
        prefix="h4_",
    )

    assert aligned.loc[0, "h4_direction"] == "up"
