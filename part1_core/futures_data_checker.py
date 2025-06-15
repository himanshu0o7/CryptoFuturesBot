# ~/CryptoFuturesBot/part1_core/futures_data_checker.py

import json

with open('part1_core/futures_data.json', 'r') as f:
    data = json.load(f)

# Sort functions
gainers = sorted(data, key=lambda x: x['priceChangePercent'], reverse=True)
losers = sorted(data, key=lambda x: x['priceChangePercent'])
top_volume = sorted(data, key=lambda x: x['quoteVolume'], reverse=True)

# Print results
print("\n========== TOP 10 GAINERS ==========")
for i in gainers[:10]:
    print(f"{i['symbol']:10} | Change %: {i['priceChangePercent']:>7} | Last Price: {i['lastPrice']}")

print("\n========== TOP 10 LOSERS ==========")
for i in losers[:10]:
    print(f"{i['symbol']:10} | Change %: {i['priceChangePercent']:>7} | Last Price: {i['lastPrice']}")

print("\n========== TOP 10 BY VOLUME (QuoteVolume) ==========")
for i in top_volume[:10]:
    print(f"{i['symbol']:10} | Quote Volume: {i['quoteVolume']:,.2f} | Last Price: {i['lastPrice']}")

print(f"\n✅ Total symbols in data: {len(data)}")

