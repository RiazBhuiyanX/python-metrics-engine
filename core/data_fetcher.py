import ccxt
import pandas as pd

def fetch_binance_data(symbol='BTC/USDT', timeframe='5m', limit=1000):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df = df.iloc[:-1]  # remove the last incomplete candle

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Europe/Sofia')
    
    df.to_csv('data/btc_usdt_ohlcv.csv', index=False)
    return df

