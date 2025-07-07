import csv
import glob
import sys
from typing import List, Dict

BUY_SELL_THRESHOLD = 3.0
VOLUME_THRESHOLD = 10_000_000


def load_candles(path: str) -> List[Dict[str, float]]:
    candles = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                open_price = float(row.get("open") or row.get("Open"))
                close_price = float(row.get("close") or row.get("Close"))
                high = float(row.get("high") or row.get("High"))
                low = float(row.get("low") or row.get("Low"))
                volume = float(row.get("volume") or row.get("Volume"))
            except (TypeError, ValueError):
                continue
            candles.append(
                {
                    "open": open_price,
                    "close": close_price,
                    "high": high,
                    "low": low,
                    "volume": volume,
                }
            )
    return candles


def detect_signals(candles: List[Dict[str, float]]) -> List[float]:
    trades = []
    for i in range(1, len(candles) - 1):
        prev_close = candles[i - 1]["close"]
        current = candles[i]
        price_change_percent = (current["close"] - prev_close) / prev_close * 100 if prev_close != 0 else 0
        quote_volume = current["close"] * current["volume"]
        next_close = candles[i + 1]["close"]
        if (
            price_change_percent > BUY_SELL_THRESHOLD
            and quote_volume > VOLUME_THRESHOLD
        ):
            pnl = next_close - current["close"]
            trades.append(pnl)
        elif (
            price_change_percent < -BUY_SELL_THRESHOLD
            and quote_volume > VOLUME_THRESHOLD
        ):
            pnl = current["close"] - next_close
            trades.append(pnl)
    return trades


def summarize(trades: List[float]) -> None:
    total = len(trades)
    wins = sum(1 for t in trades if t > 0)
    total_pnl = sum(trades)
    win_rate = (wins / total) * 100 if total else 0
    print(f"Total Trades: {total}")
    print(f"Winning Trades: {wins}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Total PnL: {total_pnl:.2f}")


def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else "data/*.csv"
    all_trades: List[float] = []
    for file in glob.glob(pattern):
        trades = detect_signals(load_candles(file))
        all_trades.extend(trades)
    summarize(all_trades)


if __name__ == "__main__":
    main()
