import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env from current directory

api_key = os.getenv("COINSWITCH_API_KEY")
secret_key = os.getenv("COINSWITCH_SECRET_KEY")

print("✅ COINSWITCH_API_KEY:", api_key)
print("✅ COINSWITCH_SECRET_KEY:", secret_key)
print("🔢 Length of SECRET_KEY:", len(secret_key) if secret_key else "Not Found")
