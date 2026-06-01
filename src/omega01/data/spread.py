from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True)
class SpreadReport:
    symbol: str
    timeframe: str
    rows: int
    median: float
    p75: float
    p90: float
    p95: float
    p99: float
    max_spread: int
    zero_spread_rows: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def analyze_spread(frame: pd.DataFrame, symbol: str, timeframe: str) -> SpreadReport:
    if "spread" not in frame.columns:
        raise ValueError("Missing required spread column")
    spreads = pd.to_numeric(frame["spread"], errors="coerce").dropna()
    if spreads.empty:
        raise ValueError("No spread values available")

    return SpreadReport(
        symbol=symbol,
        timeframe=timeframe,
        rows=int(len(spreads)),
        median=_clean_float(spreads.quantile(0.50)),
        p75=_clean_float(spreads.quantile(0.75)),
        p90=_clean_float(spreads.quantile(0.90)),
        p95=_clean_float(spreads.quantile(0.95)),
        p99=_clean_float(spreads.quantile(0.99)),
        max_spread=int(spreads.max()),
        zero_spread_rows=int((spreads == 0).sum()),
    )


def recommend_max_spread(report: SpreadReport, minimum_buffer: int = 2) -> int:
    return int(round(max(report.p95, report.median + minimum_buffer)))


def _clean_float(value: float) -> float:
    return round(float(value), 6)
