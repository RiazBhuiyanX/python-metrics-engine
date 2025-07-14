DEFAULT_LOOKBACK = 20
def apply_trend_breakout_strategy(df, lookback=DEFAULT_LOOKBACK):
    """
    Apply a simple trend breakout strategy:
    - BUY when price breaks above previous high
    - SELL when price drops below previous low
    """    
    
    # Compute rolling highest high and lowest low over a lookback window
    df['recent_high'] = df['close'].rolling(window=lookback).max()
    df['recent_low'] = df['close'].rolling(window=lookback).min()

    # Initialize signal column (0 = hold)
    df['signal'] = 0

    # Generate signals based on breakout conditions
    df.loc[df['close'] > df['recent_high'].shift(1), 'signal'] = 1   # BUY
    df.loc[df['close'] < df['recent_low'].shift(1), 'signal'] = -1  # SELL

    # Optional: round for cleaner exports
    df[['close', 'recent_high', 'recent_low']] = df[['close', 'recent_high', 'recent_low']].round(2)

    # Save the signals to CSV for inspection
    df[['timestamp', 'close', 'recent_high', 'recent_low', 'signal']].to_csv('signals/btc_signals_trend_breakout.csv', index=False)

    return df
