from __future__ import annotations

import argparse
from pathlib import Path

from omega01.data.mt5_inventory import (
    InventoryRequest,
    SymbolInfo,
    collect_timeframe_inventory,
    discover_forex_symbols,
    parse_timeframes,
    write_inventory_csv,
)
from omega01.paths import REPORTS_DIR


class MT5InventoryClient:
    def __init__(self, terminal_path: str | None = None) -> None:
        try:
            import MetaTrader5 as mt5
        except ImportError as exc:
            raise SystemExit(
                "MetaTrader5 package is not installed. Run: "
                'pip install -e ".[dev,mt5]"'
            ) from exc

        self.mt5 = mt5
        self.terminal_path = terminal_path

    def __enter__(self) -> "MT5InventoryClient":
        initialized = (
            self.mt5.initialize(path=self.terminal_path)
            if self.terminal_path
            else self.mt5.initialize()
        )
        if not initialized:
            code, message = self.mt5.last_error()
            raise SystemExit(f"MT5 initialize failed: {code} {message}")
        return self

    def __exit__(self, *_args: object) -> None:
        self.mt5.shutdown()

    def symbols(self) -> list[SymbolInfo]:
        raw_symbols = self.mt5.symbols_get()
        if raw_symbols is None:
            code, message = self.mt5.last_error()
            raise SystemExit(f"MT5 symbols_get failed: {code} {message}")
        return [
            SymbolInfo(
                name=item.name,
                path=getattr(item, "path", ""),
                visible=bool(getattr(item, "visible", False)),
            )
            for item in raw_symbols
        ]

    def copy_rates(self, symbol: str, timeframe: str, bars: int):
        timeframe_value = getattr(self.mt5, f"TIMEFRAME_{timeframe}", None)
        if timeframe_value is None:
            raise ValueError(f"Unsupported MT5 timeframe: {timeframe}")
        return self.mt5.copy_rates_from_pos(symbol, timeframe_value, 0, bars)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inventory forex symbols from MT5/Exness.")
    parser.add_argument("--terminal-path", default=None, help="Optional path to terminal64.exe.")
    parser.add_argument(
        "--timeframes",
        default="M5,M15,H1,H4,D1",
        help="Comma-separated MT5 timeframes. Default: M5,M15,H1,H4,D1.",
    )
    parser.add_argument("--bars", type=int, default=5000, help="Bars to inspect per timeframe.")
    parser.add_argument(
        "--out",
        default=str(REPORTS_DIR / "mt5_forex_inventory.csv"),
        help="CSV output path. Defaults to reports/mt5_forex_inventory.csv.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    request = InventoryRequest(
        timeframes=parse_timeframes(args.timeframes),
        bars=args.bars,
        terminal_path=args.terminal_path,
    )

    with MT5InventoryClient(request.terminal_path) as client:
        forex_symbols = discover_forex_symbols(client.symbols())
        rows = collect_timeframe_inventory(
            client=client,
            symbols=forex_symbols,
            timeframes=request.timeframes,
            bars=request.bars,
        )

    output_path = Path(args.out)
    write_inventory_csv(rows, output_path)

    print(f"Forex symbols: {len(forex_symbols)}")
    print(f"Inventory rows: {len(rows)}")
    print(f"Wrote: {output_path}")
    if forex_symbols:
        print("First symbols: " + ", ".join(item.name for item in forex_symbols[:20]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
