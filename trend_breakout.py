def apply_trend_breakout_strategy(df, lookback=20):
    df['recent_high'] = df['close'].rolling(window=lookback).max()
    df['recent_low'] = df['close'].rolling(window=lookback).min()

    df['signal'] = 0
    df.loc[df['close'] > df['recent_high'].shift(1), 'signal'] = 1   # BUY сигнал
    df.loc[df['close'] < df['recent_low'].shift(1), 'signal'] = -1  # SELL сигнал

    df[['close', 'recent_high', 'recent_low']] = df[['close', 'recent_high', 'recent_low']].round(2)

    df[['timestamp', 'close', 'recent_high', 'recent_low', 'signal']].to_csv('btc_signals_trend_breakout.csv', index=False)

    return df
