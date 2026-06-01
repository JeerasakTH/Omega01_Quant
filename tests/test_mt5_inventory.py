from omega01.data.mt5_inventory import (
    InventoryRequest,
    SymbolInfo,
    collect_timeframe_inventory,
    discover_forex_symbols,
    normalize_symbol_name,
    parse_timeframes,
)


def test_normalize_symbol_name_removes_common_broker_suffixes() -> None:
    assert normalize_symbol_name("EURUSDm") == "EURUSD"
    assert normalize_symbol_name("GBPJPY.pro") == "GBPJPY"
    assert normalize_symbol_name("USDCHF") == "USDCHF"


def test_discover_forex_symbols_keeps_currency_pairs_and_skips_metals() -> None:
    symbols = [
        SymbolInfo(name="EURUSDm", path="Forex\\Majors\\EURUSDm", visible=True),
        SymbolInfo(name="GBPJPYm", path="Forex\\Crosses\\GBPJPYm", visible=True),
        SymbolInfo(name="XAUUSDm", path="Metals\\XAUUSDm", visible=True),
        SymbolInfo(name="US500m", path="Indices\\US500m", visible=True),
    ]

    forex = discover_forex_symbols(symbols)

    assert [item.name for item in forex] == ["EURUSDm", "GBPJPYm"]
    assert [item.base_symbol for item in forex] == ["EURUSD", "GBPJPY"]


def test_inventory_request_defaults_to_core_forex_timeframes() -> None:
    request = InventoryRequest()

    assert request.timeframes == ("M5", "M15", "H1", "H4", "D1")


def test_parse_timeframes_uppercases_and_splits_values() -> None:
    assert parse_timeframes("m5,m15,H1") == ("M5", "M15", "H1")


def test_collect_timeframe_inventory_summarizes_first_and_last_bar() -> None:
    class FakeClient:
        def copy_rates(self, symbol: str, timeframe: str, bars: int):
            assert symbol == "EURUSDm"
            assert timeframe == "M5"
            assert bars == 2
            return [{"time": 1_700_000_000}, {"time": 1_700_000_300}]

    rows = collect_timeframe_inventory(
        client=FakeClient(),
        symbols=[SymbolInfo(name="EURUSDm", path="Forex\\EURUSDm", visible=True, base_symbol="EURUSD")],
        timeframes=("M5",),
        bars=2,
    )

    assert len(rows) == 1
    assert rows[0].symbol == "EURUSDm"
    assert rows[0].base_symbol == "EURUSD"
    assert rows[0].timeframe == "M5"
    assert rows[0].bars == 2
    assert rows[0].first_time.isoformat() == "2023-11-14T22:13:20+00:00"
    assert rows[0].last_time.isoformat() == "2023-11-14T22:18:20+00:00"
