import os
from dotenv import load_dotenv

load_dotenv()
API_SECRET = os.getenv("COINSWITCH_SECRET_KEY")

if not API_SECRET:
    print("❌ Error: COINSWITCH_SECRET_KEY is not set in the environment.")
    exit(1)
elif len(API_SECRET) != 64:
    print(f"❌ Error: COINSWITCH_SECRET_KEY must be 64 characters, got {len(API_SECRET)} characters.")
    print(f"Value: {API_SECRET}")
    exit(1)
elif not all(c in "0123456789abcdefABCDEF" for c in API_SECRET):
    print("❌ Error: COINSWITCH_SECRET_KEY must be a valid hexadecimal string.")
    print(f"Value: {API_SECRET}")
    exit(1)
else:
    print("✅ COINSWITCH_SECRET_KEY is valid.")

