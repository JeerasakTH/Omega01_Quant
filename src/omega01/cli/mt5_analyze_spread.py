from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from omega01.cli.mt5_fetch_forex import DEFAULT_MAJOR_SYMBOLS, DEFAULT_TIMEFRAMES, parse_csv
from omega01.data.spread import analyze_spread, recommend_max_spread
from omega01.paths import DATA_DIR, REPORTS_DIR


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze MT5 spread distributions from local CSV data.")
    parser.add_argument(
        "--symbols",
        default=",".join(DEFAULT_MAJOR_SYMBOLS),
        help="Comma-separated MT5 symbols.",
    )
    parser.add_argument(
        "--timeframes",
        default=",".join(DEFAULT_TIMEFRAMES),
        help="Comma-separated MT5 timeframes.",
    )
    parser.add_argument(
        "--data-dir",
        default=str(DATA_DIR / "raw" / "mt5"),
        help="Local MT5 raw data directory.",
    )
    parser.add_argument(
        "--out",
        default=str(REPORTS_DIR / "mt5_spread_analysis.csv"),
        help="Spread analysis CSV output path.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    symbols = parse_csv(args.symbols)
    timeframes = tuple(item.upper() for item in parse_csv(args.timeframes))
    data_dir = Path(args.data_dir)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    for symbol in symbols:
        for timeframe in timeframes:
            input_path = data_dir / symbol / f"{symbol}_{timeframe}.csv"
            if not input_path.exists():
                records.append(
                    {
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "error": f"missing file: {input_path}",
                    }
                )
                continue
            frame = pd.read_csv(input_path)
            report = analyze_spread(frame, symbol=symbol, timeframe=timeframe)
            record = report.as_dict()
            record["recommended_max_spread"] = recommend_max_spread(report)
            record["error"] = ""
            records.append(record)
            print(
                f"{symbol} {timeframe}: median={report.median:g} "
                f"p95={report.p95:g} recommended={record['recommended_max_spread']}"
            )

    pd.DataFrame.from_records(records).to_csv(output_path, index=False)
    print(f"Wrote spread analysis: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
