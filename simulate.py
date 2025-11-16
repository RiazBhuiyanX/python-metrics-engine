import os
import pandas as pd
import argparse
from core.data_fetcher import fetch_binance_data
from core.metrics import calculate_metrics
from strategies.mean_reversion import apply_mean_reversion_strategy
from strategies.momentum import apply_momentum_strategy
from strategies.trend_breakout import apply_trend_breakout_strategy

# =======================
# Constants
# =======================
INITIAL_BALANCE = 1000  # Starting USDT balance
STOP_LOSS_RATIO = 0.8  # Stop trading if balance drops below 80%
SCALED_BUY_RATIO = 0.95  # In scaled mode: buy with 95% of available USDT
SCALED_SELL_RATIO = 0.05  # In scaled mode: sell 5% of BTC holdings
MIN_USDT_FOR_TRADE = 10  # Minimum USDT required to execute a buy in scaled mode


def get_strategy_func(strategy_name):
    """Maps strategy name string to its corresponding function."""
    if strategy_name == "mean_reversion":
        return apply_mean_reversion_strategy
    elif strategy_name == "momentum":
        return apply_momentum_strategy
    elif strategy_name == "trend_breakout":
        return apply_trend_breakout_strategy
    return None


def simulate_trading(df, mode="all_in", strategy="unknown"):
    balance_usdt = INITIAL_BALANCE
    balance_btc = 0
    stop_threshold = INITIAL_BALANCE * STOP_LOSS_RATIO
    stop_triggered = False
    results = []

    for _, row in df.iterrows():
        signal = row["signal"]
        price = row["close"]

        # =======================
        # BUY Logic
        # =======================
        if signal == 1:
            if mode == "all_in" and balance_usdt > 0:
                # Use entire USDT balance to buy BTC
                buy_amount = balance_usdt
                btc_bought = buy_amount / price
                balance_btc += btc_bought
                balance_usdt -= buy_amount
            elif mode == "scaled" and balance_usdt > MIN_USDT_FOR_TRADE:
                # Buy BTC with 95% of current USDT balance
                buy_amount = balance_usdt * SCALED_BUY_RATIO
                btc_bought = buy_amount / price
                balance_btc += btc_bought
                balance_usdt -= buy_amount

        # =======================
        # SELL Logic
        # =======================
        elif signal == -1:
            if mode == "all_in" and balance_btc > 0:
                # Sell entire BTC balance
                balance_usdt += balance_btc * price
                balance_btc = 0
            elif mode == "scaled" and balance_btc > 0:
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
            signal = 0  # Ignore further signals

        # =======================
        # Save Trade State
        # =======================
        results.append(
            {
                "timestamp": row["timestamp"],
                "price": round(price, 2),
                "signal": signal,
                "balance_usdt": round(balance_usdt, 2),
                "balance_btc": round(balance_btc, 6),
                "total_balance_usdt": round(total_balance_usdt, 2),
                "stop_triggered": stop_triggered,
                "strategy": strategy,
                "mode": mode,
            }
        )

    # =======================
    # Final Summary
    # =======================
    final_price = df.iloc[-1]["close"]
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
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python Simulation Engine for Algorithmic Analysis."
    )
    parser.add_argument(
        "--strategy",
        type=str,
        default="all",
        choices=["all", "mean_reversion", "momentum", "trend_breakout"],
        help="Strategy to run.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="all",
        choices=["all", "all_in", "scaled"],
        help="Execution mode (All-In or Scaled).",
    )
    args = parser.parse_args()

    # 1. Fetch data (once)
    df_raw = fetch_binance_data()
    if df_raw.empty:
        print("Exiting: Could not fetch data.")
        exit()

    # List of strategies to process
    strategies_to_run = (
        ["mean_reversion", "momentum", "trend_breakout"]
        if args.strategy == "all"
        else [args.strategy]
    )

    # List of modes to process
    modes_to_run = ["all_in", "scaled"] if args.mode == "all" else [args.mode]

    # 2. Run simulation pipeline
    for strategy_name in strategies_to_run:
        strategy_func = get_strategy_func(strategy_name)
        if strategy_func:
            df_signals = strategy_func(df_raw.copy())

            for mode_name in modes_to_run:
                # Run the simulation for the given signal and mode
                simulate_trading(
                    df_signals.copy(), mode=mode_name, strategy=strategy_name
                )
