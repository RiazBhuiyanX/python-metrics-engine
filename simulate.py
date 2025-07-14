import os
import pandas as pd
from core.data_fetcher import fetch_binance_data
from core.metrics import calculate_metrics
from strategies.mean_reversion import apply_mean_reversion_strategy
from strategies.momentum import apply_momentum_strategy
from strategies.trend_breakout import apply_trend_breakout_strategy

# =======================
# Constants
# =======================
INITIAL_BALANCE = 1000                 # Starting USDT balance
STOP_LOSS_RATIO = 0.8                  # Stop trading if balance drops below 80%
SCALED_BUY_RATIO = 0.95                # In scaled mode: buy with 95% of available USDT
SCALED_SELL_RATIO = 0.05               # In scaled mode: sell 5% of BTC holdings
MIN_USDT_FOR_TRADE = 10                # Minimum USDT required to execute a buy in scaled mode

def simulate_trading(df, mode='all_in', strategy='unknown'):
    balance_usdt = INITIAL_BALANCE
    balance_btc = 0
    stop_threshold = INITIAL_BALANCE * STOP_LOSS_RATIO
    stop_triggered = False
    results = []

    for _, row in df.iterrows():
        signal = row['signal']
        price = row['close']

        # =======================
        # BUY Logic
        # =======================
        if signal == 1:
            if mode == 'all_in' and balance_usdt > 0:
                # Use entire USDT balance to buy BTC                
                buy_amount = balance_usdt 
                btc_bought = buy_amount / price
                balance_btc += btc_bought
                balance_usdt -= buy_amount
            elif mode == 'scaled' and balance_usdt > MIN_USDT_FOR_TRADE:
                # Buy BTC with 95% of current USDT balance
                buy_amount = balance_usdt * SCALED_BUY_RATIO
                btc_bought = buy_amount / price
                balance_btc += btc_bought
                balance_usdt -= buy_amount

        # =======================
        # SELL Logic
        # =======================
        elif signal == -1:
            if mode == 'all_in' and balance_btc > 0:
                # Sell entire BTC balance
                balance_usdt += balance_btc * price
                balance_btc = 0
            elif mode == 'scaled' and balance_btc > 0:
                # Sell 5% of current BTC holdings
                sell_amount = balance_btc * SCALED_SELL_RATIO
                balance_usdt += sell_amount * price
                balance_btc -= sell_amount
        
        # =======================
        # Portfolio Value & Stop Condition
        # =======================        
        total_balance_usdt = balance_usdt + balance_btc * price

        if total_balance_usdt < stop_threshold:
            stop_triggered = True  # Stop-loss rule triggered
        
        if stop_triggered:
            signal = 0 # Ignore further signals

        # =======================
        # Save Trade State
        # =======================
        results.append({
            'timestamp': row['timestamp'],
            'price': round(price, 2),
            'signal': signal,
            'balance_usdt': round(balance_usdt, 2),
            'balance_btc': round(balance_btc, 6),
            'total_balance_usdt': round(total_balance_usdt, 2),
            'stop_triggered': stop_triggered,
            'strategy': strategy,
            'mode': mode
        })

    # =======================
    # Final Summary
    # =======================
    final_price = df.iloc[-1]['close']
    final_balance = balance_usdt + balance_btc * final_price

    print(f"\nStrategy: {strategy.upper()}")
    print(f"Mode: {mode.upper()}")
    print(f"Starting balance: {INITIAL_BALANCE} USDT")
    print(f"Final balance: {round(final_balance, 2)} USDT")
    print(f"Profit: {round(final_balance - INITIAL_BALANCE, 2)} USDT")

    # =======================
    # Save Results & Metrics
    # =======================
    results_df = pd.DataFrame(results)
    filename = f"output/simulation_{strategy}_{mode}.csv"
    results_df.to_csv(filename, index=False)

    metrics = calculate_metrics(results_df)

    print("Performance metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
    

# =======================
# Entry Point
# =======================  
if __name__ == '__main__':
    df = fetch_binance_data()

    # Run Mean Reversion strategy
    df_reversion = apply_mean_reversion_strategy(df.copy())
    simulate_trading(df_reversion, mode='all_in', strategy='mean_reversion')
    simulate_trading(df_reversion, mode='scaled', strategy='mean_reversion')

    # Run Momentum strategy
    df_momentum = apply_momentum_strategy(df.copy())
    simulate_trading(df_momentum, mode='all_in', strategy='momentum')
    simulate_trading(df_momentum, mode='scaled', strategy='momentum')

    # Run Trend Breakout strategy
    df_breakout = apply_trend_breakout_strategy(df.copy())
    simulate_trading(df_breakout, mode='all_in', strategy='trend_breakout')
    simulate_trading(df_breakout, mode='scaled', strategy='trend_breakout')

