def get_live_price(symbol):
    import requests
    url = f"https://api.coinswitch.co/v2/price?symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('price')
    raise Exception("Failed to fetch live price")

# 3. Order Placement (Mocked for now)
def place_order(symbol, qty, side="BUY"):
    print(f"Placing {side} order: {qty} of {symbol}")
    return {"status": "success", "order_id": "ORDER12345"}
