from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from omega01.cli.mt5_forex_inventory import MT5InventoryClient
from omega01.data.quality import check_ohlcv_quality
from omega01.paths import DATA_DIR, REPORTS_DIR


DEFAULT_MAJOR_SYMBOLS = (
    "EURUSDm",
    "GBPUSDm",
    "USDJPYm",
    "USDCHFm",
    "USDCADm",
    "AUDUSDm",
    "NZDUSDm",
)
DEFAULT_TIMEFRAMES = ("M5", "M15", "H1", "H4", "D1")


def parse_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def rates_to_frame(rates) -> pd.DataFrame:
    frame = pd.DataFrame(rates)
    if frame.empty:
        return frame
    frame["time"] = pd.to_datetime(frame["time"], unit="s", utc=True)
    return frame


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch forex OHLCV history from MT5.")
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
    parser.add_argument("--bars", type=int, default=10000, help="Bars to fetch per symbol/timeframe.")
    parser.add_argument("--terminal-path", default=None, help="Optional path to terminal64.exe.")
    parser.add_argument(
        "--data-dir",
        default=str(DATA_DIR / "raw" / "mt5"),
        help="Output directory for local CSV datasets.",
    )
    parser.add_argument(
        "--report",
        default=str(REPORTS_DIR / "mt5_forex_quality.csv"),
        help="Output quality report CSV path.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    symbols = parse_csv(args.symbols)
    timeframes = tuple(item.upper() for item in parse_csv(args.timeframes))
    data_dir = Path(args.data_dir)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    reports = []
    with MT5InventoryClient(args.terminal_path) as client:
        for symbol in symbols:
            for timeframe in timeframes:
                rates = client.copy_rates(symbol, timeframe, args.bars)
                frame = rates_to_frame(rates)
                symbol_dir = data_dir / symbol
                symbol_dir.mkdir(parents=True, exist_ok=True)
                output_path = symbol_dir / f"{symbol}_{timeframe}.csv"
                frame.to_csv(output_path, index=False)

                quality = check_ohlcv_quality(frame, symbol=symbol, timeframe=timeframe)
                record = quality.as_dict()
                record["path"] = str(output_path)
                reports.append(record)
                print(
                    f"{symbol} {timeframe}: rows={quality.rows} "
                    f"gaps={quality.gaps} passed={quality.passed}"
                )

    report_frame = pd.DataFrame.from_records(reports)
    report_frame.insert(0, "run_time_utc", datetime.now(UTC).isoformat())
    report_frame.to_csv(report_path, index=False)
    print(f"Wrote quality report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
