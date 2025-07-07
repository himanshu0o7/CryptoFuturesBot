# env_utils.py
from dotenv import load_dotenv
import os

def check_required_env_vars(required_vars):
    load_dotenv()
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
    return {var: os.getenv(var) for var in required_vars}

# Example usage in check_env.py
from env_utils import check_required_env_vars

try:
    env_vars = check_required_env_vars(['COINSWITCH_SECRET_KEY'])
    print(f"Secret Key: {env_vars['COINSWITCH_SECRET_KEY']}")
    print(f"Length: {len(env_vars['COINSWITCH_SECRET_KEY'])}")
except ValueError as e:
    print(f"Error: {e}")

