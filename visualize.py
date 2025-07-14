import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_summary_comparison():
    """
    Plot total USDT balance over time for all strategies and modes (summary view).
    """
    files = {
        'Mean Reversion (All-In)': 'output/simulation_mean_reversion_all_in.csv',
        'Mean Reversion (Scaled)': 'output/simulation_mean_reversion_scaled.csv',
        'Momentum (All-In)': 'output/simulation_momentum_all_in.csv',
        'Momentum (Scaled)': 'output/simulation_momentum_scaled.csv',
        'Trend Breakout (All-In)': 'output/simulation_trend_breakout_all_in.csv',
        'Trend Breakout (Scaled)': 'output/simulation_trend_breakout_scaled.csv',
    }

    plt.figure(figsize=(14, 7))


    for label, path in files.items():
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=['timestamp'])
            final_balance = df['total_balance_usdt'].iloc[-1]
            new_label = f"{label} — Final: {final_balance:.2f} USDT"
            plt.plot(df['timestamp'], df['total_balance_usdt'], label=new_label, marker='o', markevery=[0, -1])
        else:
            print(f"File not found: {path}")


    plt.title('Comparison of Trading Strategies — Total USDT Balance')
    plt.xlabel('Time')
    plt.ylabel('Balance (USDT)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/strategy_comparison.png", dpi=300)
    plt.show()


def plot_strategy_breakdown(strategy_name):
    """
    Plot a breakdown for one strategy in both All-In and Scaled modes.
    """
    modes = ['all_in', 'scaled']
    plt.figure(figsize=(12, 6))

    for mode in modes:
        filename = f"output/simulation_{strategy_name}_{mode}.csv"
        if os.path.exists(filename):
            df = pd.read_csv(filename, parse_dates=['timestamp'])
            label = f"{mode.upper()} — Final: {df['total_balance_usdt'].iloc[-1]:.2f} USDT"
            plt.plot(df['timestamp'], df['total_balance_usdt'], label=label, marker='o', markevery=[0, -1])
        else:
            print(f"File not found: {filename}")

    strategy_title = strategy_name.replace("_", " ").title()
    plt.title(f"{strategy_title}: ALL-IN vs SCALED")
    plt.xlabel("Time")
    plt.ylabel("Balance (USDT)")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"output/breakdown_{strategy_name}.png", dpi=300)
    plt.show()

def plot_drawdown(path, label):
    """
    Plot drawdown over time for a single strategy/mode.
    """    
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    df = pd.read_csv(path, parse_dates=['timestamp'])
    balance = df['total_balance_usdt']
    timestamp = df['timestamp']

    cummax = balance.cummax()
    drawdown = (balance - cummax) / cummax

    plt.figure(figsize=(12, 5))
    plt.plot(timestamp, drawdown * 100, color='red')
    plt.title(f'Drawdown Over Time — {label}')
    plt.xlabel('Time')
    plt.ylabel('Drawdown (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f"output/drawdown_{label.lower().replace(' ', '_')}.png"
    plt.savefig(filename, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Plot overall strategy comparison
    plot_summary_comparison()

    # Plot individual strategy breakdowns
    plot_strategy_breakdown("mean_reversion")
    plot_strategy_breakdown("momentum")
    plot_strategy_breakdown("trend_breakout")

    # Plot drawdowns for all strategies/modes
    plot_drawdown("output/simulation_mean_reversion_all_in.csv", "Mean Reversion All-In")
    plot_drawdown("output/simulation_mean_reversion_scaled.csv", "Mean Reversion Scaled")
    plot_drawdown("output/simulation_momentum_all_in.csv", "Momentum All-In")
    plot_drawdown("output/simulation_momentum_scaled.csv", "Momentum Scaled")
    plot_drawdown("output/simulation_trend_breakout_all_in.csv", "Trend Breakout All-In")
    plot_drawdown("output/simulation_trend_breakout_scaled.csv", "Trend Breakout Scaled")