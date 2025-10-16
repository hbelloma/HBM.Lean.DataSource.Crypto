import requests
import json
from datetime import datetime, timedelta
import os

# Example: Download daily BTC data from CoinGecko API
def download_data(symbol, start_date, end_date):
    base_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
    params = {
        'vs_currency': 'usd',
        'from': int(start_date.timestamp()),
        'to': int(end_date.timestamp())
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("API error")
    
    data = response.json()['prices']
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/{symbol}.csv", 'w') as f:
        f.write("timestamp,open,high,low,close,volume\n")
        for point in data:
            ts = datetime.fromtimestamp(point[0]/1000).strftime('%Y-%m-%d')
            price = point[1]  # Simplified; fetch OHLCV properly if needed
            f.write(f"{ts},{price},{price},{price},{price},0\n")  # Placeholder; adapt to real API

# Usage: Download last 1 year
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
download_data("bitcoin", start_date, end_date)