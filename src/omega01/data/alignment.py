from __future__ import annotations

import pandas as pd

from omega01.data.quality import timeframe_to_timedelta


def align_completed_higher_timeframe(
    entry_frame: pd.DataFrame,
    higher_frame: pd.DataFrame,
    higher_timeframe: str,
    columns: list[str],
    prefix: str = "",
) -> pd.DataFrame:
    entry = entry_frame.copy()
    higher = higher_frame.copy()

    entry["time"] = pd.to_datetime(entry["time"], utc=True)
    higher["time"] = pd.to_datetime(higher["time"], utc=True)
    higher["available_time"] = higher["time"] + timeframe_to_timedelta(higher_timeframe)

    rename_map = {column: f"{prefix}{column}" for column in columns}
    higher_features = higher[["available_time", *columns]].rename(columns=rename_map)

    aligned = pd.merge_asof(
        entry.sort_values("time"),
        higher_features.sort_values("available_time"),
        left_on="time",
        right_on="available_time",
        direction="backward",
    )
    return aligned.drop(columns=["available_time"])
