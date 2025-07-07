def place_order(symbol, qty, side="BUY"):
  print(f"[ORDER MOCK] {side} {qty} of {symbol}")
  return {"status": "success", "order_id": f"{symbol}-{side}-MOCK123"}
