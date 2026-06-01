from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from omega01.cli.mt5_fetch_forex import DEFAULT_MAJOR_SYMBOLS, DEFAULT_TIMEFRAMES, parse_csv
from omega01.data.quality import audit_ohlcv_gaps
from omega01.paths import DATA_DIR, REPORTS_DIR


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit unexpected open-market gaps in local MT5 CSV data.")
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
        default=str(REPORTS_DIR / "mt5_gap_audit.csv"),
        help="Gap audit CSV output path.",
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
                        "previous_time": "",
                        "next_time": "",
                        "missing_open_bars": "",
                        "error": f"missing file: {input_path}",
                    }
                )
                continue
            frame = pd.read_csv(input_path)
            gaps = audit_ohlcv_gaps(frame, symbol=symbol, timeframe=timeframe)
            for gap in gaps:
                gap["error"] = ""
            records.extend(gaps)
            print(f"{symbol} {timeframe}: gaps={len(gaps)}")

    pd.DataFrame.from_records(records).to_csv(output_path, index=False)
    print(f"Wrote gap audit: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
