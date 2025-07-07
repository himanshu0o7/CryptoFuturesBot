# part1_core/order_placer.py
import json
from coinswitch_api_utils import send_request


def place_order(symbol, side, quantity, price=None, order_type="market", confirm=False):
    payload = {
        "side": side.lower(),
        "symbol": symbol,
        "type": order_type,
        "exchange": "coinswitchx",
    }

    if order_type == "limit":
        payload["price"] = price

    payload["quantity"] = quantity

    if confirm:
        response = send_request("POST", "/trade/api/v2/order", payload=payload)

        if response and "data" in response:
            print(f"[SUCCESS] Order placed: {response['data']}")
        else:
            print(f"[ERROR] Failed to place order for {symbol}")
    else:
        print(
            f"[INFO] Would place order -> Symbol: {symbol}, Side: {side}, Qty: {quantity}, Type: {order_type}, Price: {price if price else 'Market'}"
        )


def main():
    try:
        with open("signal_generator.json") as f:
            signals = json.load(f)
    except FileNotFoundError:
        print("[ERROR] signal_generator.json not found! Run signal_generator.py first.")
        return

    # Example: Fixed qty = 10 USDT worth
    FIXED_QTY = 10

    for signal in signals["buy"]:
        print(f"[BUY ] Preparing order for {signal['symbol']}")
        place_order(signal["symbol"], "buy", FIXED_QTY, confirm=False)

    for signal in signals["sell"]:
        print(f"[SELL] Preparing order for {signal['symbol']}")
        place_order(signal["symbol"], "sell", FIXED_QTY, confirm=False)


if __name__ == "__main__":
    main()
