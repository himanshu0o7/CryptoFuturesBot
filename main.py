import os
import time
from dotenv import load_dotenv

from utils.risk_management import RiskManager
from utils.telegram_alert import send_telegram_alert
from utils.error_handler import retry

# ==== Load Environment ====
load_dotenv()
API_KEY = os.getenv("COINSWITCH_API_KEY")
API_SECRET = os.getenv("COINSWITCH_API_SECRET")

# ==== Price Fetch ====
def get_live_price(symbol="BTCUSDT"):
    import requests
    url = f"https://api.coinswitch.co/v2/price?symbol={symbol}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return float(response.json().get('price'))

# ==== Order Placement (Mocked) ====
def place_order(symbol, qty, side="BUY"):
    print(f"[ORDER MOCK] {side} {qty} {symbol}")
    return {"status": "success", "order_id": f"{symbol}-{side}-MOCK"}

# ==== Main Bot Logic ====
if __name__ == "__main__":
    try:
        symbol = "BTCUSDT"
        qty = 10

        print("🚀 Bot Starting...")
        send_telegram_alert("🟢 CryptoFuturesBot started.")

        entry_price = retry(lambda: get_live_price(symbol), label="Fetch Entry Price")
        print(f"✅ Entry price: ₹{entry_price}")

        order = retry(lambda: place_order(symbol, qty, "BUY"), label="Place Order")
        print(f"📦 Order Placed: {order['order_id']}")

        time.sleep(5)  # Simulate trade holding

        current_price = retry(lambda: get_live_price(symbol), label="Fetch Exit Price")
        print(f"📈 Current price: ₹{current_price}")

        rm = RiskManager(sl_pct=0.02, tp_pct=0.04)
        decision = rm.should_exit(entry_price, current_price)

        if decision:
            msg = f"🔔 {decision} Triggered!\n{symbol} moved ₹{entry_price} → ₹{current_price}"
            print(msg)
            send_telegram_alert(msg)
        else:
            print("🟡 HOLD — SL/TP not yet triggered.")
            send_telegram_alert(f"ℹ️ {symbol} HOLD — ₹{entry_price} → ₹{current_price}")

    except Exception as e:
        print(f"❌ Bot terminated: {e}")
        send_telegram_alert(f"❌ CryptoFuturesBot crashed:\n{e}")
