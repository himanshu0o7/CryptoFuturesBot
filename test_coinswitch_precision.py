import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)

# Mocked precision data for exchanges
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


def fetch_precision(exchange: str) -> dict:
    """
    Simulates an API call to fetch precision details for the given exchange.

    Args:
        exchange (str): The name of the exchange (e.g., 'coinswitchx', 'wazirx')

    Returns:
        dict: Precision data if exchange is found, else empty dict
    """
    logging.info(f"Simulating API call for exchange: {exchange}")
    precision_data = mocked_precision_data.get(exchange)
    if precision_data:
        logging.info(
            f"Exchange Precision for {exchange}: {json.dumps(precision_data, indent=2)}"
        )
        return precision_data
    else:
        logging.error(f"Exchange '{exchange}' not found in mock data.")
        return {}


if __name__ == "__main__":
    for exchange in mocked_precision_data:
        fetch_precision(exchange)
