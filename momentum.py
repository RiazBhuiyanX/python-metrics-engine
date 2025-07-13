def apply_momentum_strategy(df, short_window=10, long_window=50):
    df['sma_short'] = df['close'].rolling(window=short_window).mean()
    df['sma_long'] = df['close'].rolling(window=long_window).mean()

    df['signal'] = 0
    df.loc[df['sma_short'] > df['sma_long'], 'signal'] = 1    # BUY
    df.loc[df['sma_short'] < df['sma_long'], 'signal'] = -1   # SELL

    df[['close', 'sma_short', 'sma_long']] = df[['close', 'sma_short', 'sma_long']].round(2)
    df[['timestamp', 'close', 'sma_short', 'sma_long', 'signal']].to_csv('btc_signals_momentum.csv', index=False)

    return df