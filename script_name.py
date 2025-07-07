# ✅ Now that python-dotenv is installed, use this to test loading

import os
from dotenv import load_dotenv

load_dotenv()

print("COINSWITCH_API_KEY:", os.getenv("COINSWITCH_API_KEY"))
print("COINSWITCH_SECRET_KEY:", os.getenv("COINSWITCH_SECRET_KEY"))
