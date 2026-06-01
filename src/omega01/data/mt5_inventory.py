from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable, Protocol, Sequence

import pandas as pd


MAJOR_CURRENCIES = frozenset({"AUD", "CAD", "CHF", "EUR", "GBP", "JPY", "NZD", "USD"})
DEFAULT_TIMEFRAMES = ("M5", "M15", "H1", "H4", "D1")
COMMON_SUFFIXES = ("m", ".m", ".pro", "pro", ".raw", "raw", ".ecn", "ecn", ".std", "std")


@dataclass(frozen=True)
class SymbolInfo:
    name: str
    path: str
    visible: bool
    base_symbol: str | None = None


@dataclass(frozen=True)
class InventoryRequest:
    symbols: tuple[str, ...] = ()
    timeframes: tuple[str, ...] = DEFAULT_TIMEFRAMES
    bars: int = 5000
    terminal_path: str | None = None


@dataclass(frozen=True)
class TimeframeInventory:
    symbol: str
    base_symbol: str
    timeframe: str
    bars: int
    first_time: datetime | None
    last_time: datetime | None


class RatesClient(Protocol):
    def copy_rates(self, symbol: str, timeframe: str, bars: int): ...


def normalize_symbol_name(name: str) -> str:
    normalized = name.strip().upper()
    for suffix in COMMON_SUFFIXES:
        if normalized.endswith(suffix.upper()):
            candidate = normalized[: -len(suffix)]
            if len(candidate) >= 6:
                return candidate
    return normalized


def is_forex_base_symbol(symbol: str) -> bool:
    if len(symbol) != 6:
        return False
    base = symbol[:3]
    quote = symbol[3:]
    return base in MAJOR_CURRENCIES and quote in MAJOR_CURRENCIES and base != quote


def discover_forex_symbols(symbols: Iterable[SymbolInfo]) -> list[SymbolInfo]:
    discovered: list[SymbolInfo] = []
    seen: set[str] = set()

    for symbol in symbols:
        base_symbol = normalize_symbol_name(symbol.name)
        path = symbol.path.lower()
        if not is_forex_base_symbol(base_symbol):
            continue
        if "metal" in path or "crypto" in path or "indice" in path:
            continue
        if symbol.name in seen:
            continue
        seen.add(symbol.name)
        discovered.append(
            SymbolInfo(
                name=symbol.name,
                path=symbol.path,
                visible=symbol.visible,
                base_symbol=base_symbol,
            )
        )

    return sorted(discovered, key=lambda item: (item.base_symbol or item.name, item.name))


def write_inventory_csv(rows: Sequence[TimeframeInventory], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    records = [
        {
            "symbol": row.symbol,
            "base_symbol": row.base_symbol,
            "timeframe": row.timeframe,
            "bars": row.bars,
            "first_time": row.first_time.isoformat() if row.first_time else "",
            "last_time": row.last_time.isoformat() if row.last_time else "",
        }
        for row in rows
    ]
    pd.DataFrame.from_records(records).to_csv(output_path, index=False)


def utc_from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(int(timestamp), tz=UTC)


def parse_timeframes(value: str) -> tuple[str, ...]:
    return tuple(item.strip().upper() for item in value.split(",") if item.strip())


def collect_timeframe_inventory(
    client: RatesClient,
    symbols: Sequence[SymbolInfo],
    timeframes: Sequence[str],
    bars: int,
) -> list[TimeframeInventory]:
    rows: list[TimeframeInventory] = []
    for symbol in symbols:
        for timeframe in timeframes:
            rates = client.copy_rates(symbol.name, timeframe, bars)
            if rates is None or len(rates) == 0:
                rows.append(
                    TimeframeInventory(
                        symbol=symbol.name,
                        base_symbol=symbol.base_symbol or normalize_symbol_name(symbol.name),
                        timeframe=timeframe,
                        bars=0,
                        first_time=None,
                        last_time=None,
                    )
                )
                continue

            first_time = utc_from_timestamp(rates[0]["time"])
            last_time = utc_from_timestamp(rates[-1]["time"])
            rows.append(
                TimeframeInventory(
                    symbol=symbol.name,
                    base_symbol=symbol.base_symbol or normalize_symbol_name(symbol.name),
                    timeframe=timeframe,
                    bars=len(rates),
                    first_time=first_time,
                    last_time=last_time,
                )
            )
    return rows
