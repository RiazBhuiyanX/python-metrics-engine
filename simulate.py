import pandas as pd
from data_fetcher import fetch_binance_data
from mean_reversion import apply_mean_reversion_strategy

def simulate_trading(df, mode='all_in'):
    initial_balance = 1000
    balance_usdt = initial_balance
    balance_btc = 0
    entry_price = None
    stop_threshold = initial_balance * 0.8  # if fall under this threshold, trigger stop (80% of initial balance)
    stop_triggered = False 
    results = []

    for _, row in df.iterrows():
        signal = row['signal']
        price = row['close']

        # BUY logic
        if signal == 1:
            if mode == 'all_in' and balance_usdt > 0:
                buy_amount = balance_usdt 
                btc_bought = buy_amount / price
                balance_btc += btc_bought
                balance_usdt -= buy_amount
            elif mode == 'scaled' and balance_usdt > 10:
                buy_amount = balance_usdt * 0.95
                btc_bought = buy_amount / price
                balance_btc += btc_bought
                balance_usdt -= buy_amount
                entry_price = price if not entry_price else entry_price

        # SELL logic
        elif signal == -1:
            if mode == 'all_in' and balance_btc > 0:
                balance_usdt += balance_btc * price
                balance_btc = 0
                entry_price = None
            elif mode == 'scaled' and balance_btc > 0:
                sell_amount = balance_btc * 0.05
                balance_usdt += sell_amount * price
                balance_btc -= sell_amount
                if balance_btc == 0:
                    entry_price = None

        
        total_balance_usdt = balance_usdt + balance_btc * price

        # Stop logic
        if total_balance_usdt < stop_threshold:
            stop_triggered = True  # trigger stop
        
        if stop_triggered:
            signal = 0

        # Save all steps
        results.append({
            'timestamp': row['timestamp'],
            'price': round(price, 2),
            'signal': signal,
            'balance_usdt': round(balance_usdt, 2),
            'balance_btc': round(balance_btc, 6),
            'total_balance_usdt': round(total_balance_usdt, 2),
            'stop_triggered': stop_triggered
        })


    final_price = df.iloc[-1]['close']
    final_balance = balance_usdt + balance_btc * final_price

    print(f"\nMode: {mode.upper()}")
    print(f"Starting balance: {initial_balance} USDT")
    print(f"Final balance: {round(final_balance, 2)} USDT")
    print(f"Profit: {round(final_balance - initial_balance, 2)} USDT")

    results_df = pd.DataFrame(results)
    results_df.to_csv('trading_simulation.csv', index=False)


if __name__ == '__main__':
    df = fetch_binance_data()
    df = apply_mean_reversion_strategy(df)
    
    simulate_trading(df, mode='all_in')
    simulate_trading(df, mode='scaled')
