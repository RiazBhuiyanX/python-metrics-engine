DEFAULT_SMA_WINDOW = 10     
DEFAULT_THRESHOLD = 0.2            
def apply_mean_reversion_strategy(df, sma_window=DEFAULT_SMA_WINDOW, threshold=DEFAULT_THRESHOLD):
    """
    Apply a mean reversion strategy:
    - BUY when price is below SMA by more than a threshold (%)
    - SELL when price is above SMA by more than a threshold (%)
    """

    # Calculate SMA and percentage deviation from it
    df['sma_20'] = df['close'].rolling(window=sma_window).mean()
    df['diff'] = df['close'] - df['sma_20']
    df['percent_diff'] = (df['diff'] / df['sma_20']) * 100

    # Initialize signal column
    df['signal'] = 0

    # Mean reversion logic
    df.loc[df['percent_diff'] < -threshold, 'signal'] = 1     # BUY
    df.loc[df['percent_diff'] > threshold, 'signal'] = -1     # SELL

    # Optional: round key columns for cleaner export
    df[['close', 'sma_20', 'diff', 'percent_diff']] = df[['close', 'sma_20', 'diff', 'percent_diff']].round(2)

    # Save to CSV for visual inspection
    df[['timestamp', 'close', 'sma_20', 'diff', 'percent_diff', 'signal']].to_csv('signals/btc_signals_mean_reversion.csv', index=False)
    
    return df
