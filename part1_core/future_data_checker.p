import json
import logging

logging.basicConfig(level=logging.INFO)

# Load JSON data
try:
    logging.info("Loading saved futures_data.json...")
    with open("futures_data.json", "r") as f:
        data = json.load(f)
except (json.JSONDecodeError, FileNotFoundError) as e:
    logging.error(f"Error loading JSON: {e}")
    data = []

# Validate and prepare data
valid_items = []

if isinstance(data, list):
    for item in data:
        if isinstance(item, dict):
            symbol = item.get("symbol", "")
            open_price = item.get("openPrice", "0")
            last_price = item.get("lastPrice", "0")
            quote_volume = item.get("quoteVolume", "0")
            price_change_percent = item.get("priceChangePercent", "0")

            try:
                open_price = float(open_price)
                last_price = float(last_price)
                quote_volume = float(quote_volume)
                price_change_percent = float(price_change_percent)
            except ValueError:
                logging.warning(f"Skipping invalid item: {symbol}")
                continue

            valid_items.append({
                "symbol": symbol,
                "openPrice": open_price,
                "lastPrice": last_price,
                "quoteVolume": quote_volume,
                "priceChangePercent": price_change_percent
            })

        elif isinstance(item, str):
            logging.warning(f"Skipping string item: {item}")
        else:
            logging.warning(f"Skipping unexpected item type: {type(item)}")

elif isinstance(data, dict):
    logging.warning("Dict format detected - expecting list of items.")
    symbols = data.get("symbols", [])
    for symbol in symbols:
        logging.info(f"Symbol: {symbol}")

else:
    logging.error(f"Unexpected data format: {type(data)}")

# Now process valid_items
if valid_items:
    # Top Gainers
    print("=" * 10, "TOP 10 GAINERS", "=" * 10)
    gainers = sorted(valid_items, key=lambda x: x["priceChangePercent"], reverse=True)[:10]
    for item in gainers:
        print(f"{item['symbol']:10} | Change %: {item['priceChangePercent']:7.2f} | Last Price: {item['lastPrice']}")

    # Top Losers
    print("=" * 10, "TOP 10 LOSERS", "=" * 10)
    losers = sorted(valid_items, key=lambda x: x["priceChangePercent"])[:10]
    for item in losers:
        print(f"{item['symbol']:10} | Change %: {item['priceChangePercent']:7.2f} | Last Price: {item['lastPrice']}")

    # Top by Volume
    print("=" * 10, "TOP 10 BY VOLUME (QuoteVolume)", "=" * 10)
    top_volume = sorted(valid_items, key=lambda x: x["quoteVolume"], reverse=True)[:10]
    for item in top_volume:
        print(f"{item['symbol']:10} | Quote Volume: {item['quoteVolume']:,.2f} | Last Price: {item['lastPrice']}")
else:
    logging.warning("No valid futures data to display.")

