"""Simple backtesting placeholder"""
from .coinswitch_api import fetch_candles
from .indicators import detect_breakout


def run(symbol: str, limit: int = 200):
    data = fetch_candles(symbol, "5m", limit=limit)
    if not data or "data" not in data:
        print("No data")
        return
    candles = data["data"]
    signal = detect_breakout(candles)
    print(f"Breakout signal for {symbol}: {signal}")


if __name__ == "__main__":
    run("BTCUSDT")

