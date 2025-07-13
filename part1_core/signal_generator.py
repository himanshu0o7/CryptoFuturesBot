# part1_core/signal_generator.py
import json


def load_data():
    with open("part1_core/futures_data.json") as f:
        return json.load(f)


def generate_signals(data):
    buy_signals = []
    sell_signals = []

    for item in data:
        change = float(item.get("priceChangePercent", 0))
        symbol = item.get("symbol", "")
        quote_volume = float(item.get("quoteVolume", 0))
        last_price = float(item.get("lastPrice", 0))

        if change > 3.0 and quote_volume > 10000000:
            buy_signals.append(
                {
                    "symbol": symbol,
                    "change_percent": change,
                    "quote_volume": quote_volume,
                    "last_price": last_price,
                }
            )

        elif change < -3.0 and quote_volume > 10000000:
            sell_signals.append(
                {
                    "symbol": symbol,
                    "change_percent": change,
                    "quote_volume": quote_volume,
                    "last_price": last_price,
                }
            )

    return buy_signals, sell_signals


def save_signals(buy_signals, sell_signals):
    signals = {"buy": buy_signals, "sell": sell_signals}

    with open("signal_generator.json", "w") as f:
        json.dump(signals, f, indent=2)

    print("[SUCCESS] Signals saved to signal_generator.json")


def main():
    data = load_data()
    buy_signals, sell_signals = generate_signals(data)

    print("========================= 📈 BUY SIGNALS 📈 =========================")
    for signal in buy_signals:
        print(
            f"[BUY ] {signal['symbol']:10} | Change %: {signal['change_percent']:6.3f} | Vol: ${signal['quote_volume']:,.2f} | Last Price: {signal['last_price']}"
        )

    print("========================= 📉 SELL SIGNALS 📉 =========================")
    for signal in sell_signals:
        print(
            f"[SELL] {signal['symbol']:10} | Change %: {signal['change_percent']:6.3f} | Vol: ${signal['quote_volume']:,.2f} | Last Price: {signal['last_price']}"
        )

    save_signals(buy_signals, sell_signals)


if __name__ == "__main__":
    main()
