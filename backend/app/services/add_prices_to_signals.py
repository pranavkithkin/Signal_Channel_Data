import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import time

# Load your signal CSV
signals_df = pd.read_csv("backend/app/data/strategies.csv", parse_dates=["timestamp"])

# Binance client (no auth needed for historical data)
client = Client()

def get_symbol(coin):
    return f"{coin.upper()}USDT"

def fetch_ohlcv(symbol, start_time, interval="1m", lookahead_minutes=60*6):
    end_time = start_time + timedelta(minutes=lookahead_minutes)
    klines = client.get_historical_klines(
        symbol,
        interval,
        start_time.strftime("%d %b %Y %H:%M:%S"),
        end_time.strftime("%d %b %Y %H:%M:%S")
    )
    if not klines:
        return None
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    return df

# Add price data
results = []
for index, row in signals_df.iterrows():
    coin = row['coin']
    direction = row['direction']
    timestamp = row['timestamp']
    symbol = get_symbol(coin)

    print(f"Fetching {symbol} at {timestamp}...")

    try:
        ohlcv = fetch_ohlcv(symbol, timestamp)
        if ohlcv is None:
            continue

        entry_candle = ohlcv.iloc[0]
        future_high = ohlcv['high'].max()
        future_low = ohlcv['low'].min()

        entry_price = entry_candle['close']

        results.append({
            'timestamp': timestamp,
            'coin': coin,
            'direction': direction,
            'entry_price': entry_price,
            'future_high': future_high,
            'future_low': future_low,
            'raw_message': row['raw_message']
        })

        time.sleep(0.3)  # Prevent IP ban

    except Exception as e:
        print(f"Error with {symbol}: {e}")
        continue

# Save result
df = pd.DataFrame(results)
df.to_csv("signals_with_price_data.csv", index=False)
print(f"\n✅ Done. Saved {len(df)} signals with price data.")
