# part1_core/coinswitch_futures_pnl_tracker_enhanced.py

import json
import requests
import logging
import time
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key


def get_wallet_balance():
    endpoint = "/trade/api/v2/futures/wallet_balance"
    method = "GET"
    params = {}
    payload = {}

    epoch_time = str(int(time.time() * 1000))
    signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

    url = "https://coinswitch.co" + endpoint

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-SIGNATURE": signature,
        "X-AUTH-APIKEY": API_KEY,
        "X-AUTH-EPOCH": epoch_time,
    }

    response = requests.request("GET", url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json().get("data", {})
        return data
    else:
        logging.error(
            f"Failed to fetch wallet balance: {response.status_code} - {response.text}"
        )
        return None


def load_orders_log():
    try:
        with open("orders_log.json", "r") as f:
            orders = json.load(f)
            return orders
    except Exception as e:
        logging.error(f"Failed to load orders_log.json: {e}")
        return []


# ---- MAIN ----
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Fetching Futures Wallet Balance for Enhanced PnL Tracker...")

    wallet_data = get_wallet_balance()
    orders_log = load_orders_log()

    print("\n========== Futures PnL Tracker (Enhanced) ==========")
    print(
        f"{'Symbol':<12}{'Pos Margin':<14}{'Blocked':<10}{'Curr Price':<12}{'Entry Price':<12}{'Qty':<8}{'PnL %':<8}"
    )
    print("=" * 70)

    if wallet_data:
        assets = wallet_data.get("asset", [])
        for asset in assets:
            symbol = asset.get("symbol", "")
            pos_margin = float(asset.get("position_margin", "0"))
            blocked_balance = float(asset.get("blocked_balance", "0"))
            # Skip symbols without open positions
            if pos_margin <= 0:
                continue

            # Find matching order in orders_log.json
            matching_order = None
            for order in orders_log:
                if order.get("symbol", "").upper() == symbol.upper():
                    matching_order = order
                    break

            if matching_order:
                entry_price = float(matching_order.get("price", "0"))
                quantity = float(matching_order.get("quantity", "0"))
                side = matching_order.get("side", "BUY")

                # For demo: use blocked_balance as proxy for qty if qty=0
                if quantity == 0:
                    quantity = blocked_balance / entry_price if entry_price > 0 else 0

                # Get current price from latest wallet_balance API
                current_price = float(asset.get("current_price", "0"))
                if current_price == 0:
                    # fallback if wallet API didn't give current_price, use buy_rate
                    current_price = float(wallet_data.get("buy_rate", "0"))

                # Calculate PnL
                if side == "BUY":
                    pnl = (current_price - entry_price) * quantity
                else:  # SELL
                    pnl = (entry_price - current_price) * quantity

                try:
                    pnl_pct = (
                        (pnl / (entry_price * quantity)) * 100
                        if entry_price > 0 and quantity > 0
                        else 0
                    )
                except:
                    pnl_pct = 0

                row = f"{symbol:<12}{pos_margin:<14.4f}{blocked_balance:<10.4f}{current_price:<12.4f}{entry_price:<12.4f}{quantity:<8.4f}{pnl_pct:<8.2f}"
                print(row)
            else:
                logging.warning(
                    f"No matching order found for {symbol}, skipping PnL calc."
                )

    print("=" * 70)
    print("Completed Enhanced PnL Tracker.")
