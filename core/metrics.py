def calculate_metrics(df):
    """
    Calculate key performance metrics for a trading simulation.
    """
    balances = df['total_balance_usdt']

    # Max Drawdown (%)
    cumulative_max = balances.cummax()
    drawdown = (balances - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()


    # Total Growth (%)
    growth = (balances.iloc[-1] / balances.iloc[0] - 1) * 100

    # Simulation Duration
    start_time = df['timestamp'].iloc[0]
    end_time = df['timestamp'].iloc[-1]
    duration = end_time - start_time
    duration_str = str(duration)

    # Signal Counts
    num_buys = (df['signal'] == 1).sum()
    num_sells = (df['signal'] == -1).sum()

    # Final Metrics Summary
    return {
        'Max Drawdown %': round(max_drawdown * 100, 2),
        'Growth %': round(growth, 2),
        'Buy Signals': num_buys,
        'Sell Signals': num_sells,
        'Simulation Duration': duration_str
    }
