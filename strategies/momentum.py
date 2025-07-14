DEFAULT_SHORT_WINDOW = 10     # Fast-moving average window
DEFAULT_LONG_WINDOW = 50      # Slow-moving average window
def apply_momentum_strategy(df, short_window=DEFAULT_SHORT_WINDOW, long_window=DEFAULT_LONG_WINDOW):
    """
    Apply a basic momentum strategy using SMA crossovers:
    - BUY when short SMA crosses above long SMA
    - SELL when short SMA crosses below long SMA
    """

    # Calculate simple moving averages
    df['sma_short'] = df['close'].rolling(window=short_window).mean()
    df['sma_long'] = df['close'].rolling(window=long_window).mean()

    # Initialize signal column (0 = HOLD)
    df['signal'] = 0

    # Momentum logic:
    df.loc[df['sma_short'] > df['sma_long'], 'signal'] = 1    # BUY signal
    df.loc[df['sma_short'] < df['sma_long'], 'signal'] = -1   # SELL signal

    # Optional: round values for cleaner export
    df[['close', 'sma_short', 'sma_long']] = df[['close', 'sma_short', 'sma_long']].round(2)
    
    # Export signal CSV if enabled
    df[['timestamp', 'close', 'sma_short', 'sma_long', 'signal']].to_csv('signals/btc_signals_momentum.csv', index=False)

    return df