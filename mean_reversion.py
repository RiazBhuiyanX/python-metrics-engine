import pandas as pd

def apply_mean_reversion_strategy(df, sma_window=10, threshold=0.2):
    df['sma_20'] = df['close'].rolling(window=sma_window).mean()
    df['diff'] = df['close'] - df['sma_20']
    df['percent_diff'] = (df['diff'] / df['sma_20']) * 100

    df['signal'] = 0
    df.loc[df['percent_diff'] < -threshold, 'signal'] = 1     # BUY
    df.loc[df['percent_diff'] > threshold, 'signal'] = -1     # SELL

    df[['close', 'sma_20', 'diff', 'percent_diff']] = df[['close', 'sma_20', 'diff', 'percent_diff']].round(2)

    df[['timestamp', 'close', 'sma_20', 'diff', 'percent_diff', 'signal']].to_csv('btc_signals.csv', index=False)
    return df
