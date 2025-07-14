# 1. .env Loader & API Validation
def load_env():
    from dotenv import load_dotenv, find_dotenv
    import os

    dotenv_path = find_dotenv()
    if dotenv_path == "":
        raise FileNotFoundError(
            ".env file not found. Please ensure it exists in your root directory."
        )

    load_dotenv(dotenv_path)
    api_key = os.getenv("COINSWITCH_API_KEY")
    api_secret = os.getenv("COINSWITCH_API_SECRET")

    if not api_key:
        print("Warning: COINSWITCH_API_KEY is missing in .env")
    if not api_secret:
        print("Warning: COINSWITCH_API_SECRET is missing in .env")

    if not api_key or not api_secret:
        raise ValueError(
            "Missing CoinSwitch API credentials in .env. Please check the variable names and values."
        )

    return api_key, api_secret
