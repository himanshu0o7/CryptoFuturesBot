# ~/CryptoFuturesBot/part1_core/volume_spike_detector.py

import json

# Load futures data
with open('part1_core/futures_data.json', 'r') as f:
    data = json.load(f)

# Threshold for volume spike (customize as needed)
VOLUME_THRESHOLD_USD = 100000000  # $100 million quote volume

# Detect spikes
spikes = [s for s in data if s['quoteVolume'] > VOLUME_THRESHOLD_USD]

# Sort by volume descending
spikes = sorted(spikes, key=lambda x: x['quoteVolume'], reverse=True)

# Print results
print("\n========== VOLUME SPIKES > $100M ==========")
if spikes:
    for s in spikes:
        print(f"{s['symbol']:10} | Quote Volume: {s['quoteVolume']:,.2f} | Change %: {s['priceChangePercent']:>7} | Last Price: {s['lastPrice']}")
else:
    print("❌ No volume spikes detected.")

