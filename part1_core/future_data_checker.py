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

# Process data
symbols = []

if isinstance(data, list):
    for item in data:
        try:
            if isinstance(item, dict):
                symbol = item.get("symbol", "")
                if symbol:
                    symbols.append(symbol)
                    logging.info(f"Valid symbol found: {symbol}")
            elif isinstance(item, str):
                logging.warning(f"Skipping bad item (string): {item}")
            else:
                logging.warning(f"Skipping bad item (unknown type): {type(item)}")
        except Exception as e:
            logging.error(f"[ERROR] Error processing item: {item} - Exception: {e}")

elif isinstance(data, dict):
    logging.info("Data is a dict — trying to extract 'symbols' field...")
    symbols_list = data.get("symbols", [])
    if isinstance(symbols_list, list):
        for symbol in symbols_list:
            symbols.append(symbol)
            logging.info(f"Symbol: {symbol}")
    else:
        logging.warning("'symbols' field is not a list.")

else:
    logging.error(f"Unexpected data format: {type(data)}")

# Final output
print("\n========= VALID SYMBOLS =========")
for symbol in symbols:
    print(f"Symbol: {symbol}")

logging.info(f"Total valid symbols found: {len(symbols)}")
