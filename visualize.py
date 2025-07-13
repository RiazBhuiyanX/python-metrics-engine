import pandas as pd
import matplotlib.pyplot as plt
import os


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
