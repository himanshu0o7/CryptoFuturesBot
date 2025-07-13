import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)

# Supported exchanges (mocked for testing)
valid_exchanges = ["coinswitchx", "wazirx"]

# Mocked precision response for testing without API call
mocked_precision_data = {
    "coinswitchx": {
        "BTC": {"pricePrecision": 2, "quantityPrecision": 6},
        "ETH": {"pricePrecision": 2, "quantityPrecision": 5},
    },
    "wazirx": {
        "BTC": {"pricePrecision": 1, "quantityPrecision": 5},
        "ETH": {"pricePrecision": 2, "quantityPrecision": 4},
    },
}


def fetch_precision(exchange):
    logging.info(f"Simulating API call for exchange: {exchange}")
    precision_data = mocked_precision_data.get(exchange)
    if precision_data:
        logging.info(
            f"Exchange Precision for {exchange}: {json.dumps(precision_data, indent=2)}"
        )
    else:
        logging.error(f"Exchange '{exchange}' not found in mock data.")


if __name__ == "__main__":
    for exchange in valid_exchanges:
        logging.info(f"Fetching Exchange Precision for: {exchange}")
        fetch_precision(exchange)
