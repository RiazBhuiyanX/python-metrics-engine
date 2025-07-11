import pandas as pd
from data_fetcher import fetch_binance_data
from mean_reversion import apply_mean_reversion_strategy

def simulate_trading(df, initial_balance=1000):
    balance_usdt = initial_balance
    balance_btc = 0
    position = 'cash'

    results = []

    for _, row in df.iterrows():
        signal = row['signal']
        price = row['close']

        # BUY 
        if signal == 1 and balance_usdt > 0:
            buy_amount = balance_usdt 
            btc_bought = buy_amount / price
            balance_btc += btc_bought
            balance_usdt -= buy_amount
            position = 'btc'

        # SELL 
        elif signal == -1 and balance_btc > 0:
            balance_usdt += balance_btc * price
            balance_btc = 0
            position = 'cash'

        # Save all steps
        results.append({
            'timestamp': row['timestamp'],
            'price': round(price, 2),
            'signal': signal,
            'position': position,
            'balance_usdt': round(balance_usdt, 2),
            'balance_btc': round(balance_btc, 6)
        })

    final_price = df.iloc[-1]['close']
    final_balance = balance_usdt + balance_btc * final_price

    print(f"\nStarting balance: {initial_balance} USDT")
    print(f"Final balance: {round(final_balance, 2)} USDT")
    print(f"Profit: {round(final_balance - initial_balance, 2)} USDT")

    results_df = pd.DataFrame(results)
    results_df.to_csv('trading_simulation.csv', index=False)


if __name__ == '__main__':
    df = fetch_binance_data()
    df = apply_mean_reversion_strategy(df)
    simulate_trading(df)
