<h1 align="left">
  <img src="raven_logo_256.png" alt="Logo" width="40" style="vertical-align: middle;"/>
  Raven Quant Task
</h1>

## 📚 Table of Contents

- [🧠 Summary](#-summary)
- [⚙️ Tech Stack](#-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🛠️ How to Run](#️-how-to-run)

## ✅ Summary

This project explores whether a fixed capital of 1000 USDT can be grown through algorithmic trading on the BTC/USDT pair. I implemented three different trading strategies (**Mean Reversion**, **Momentum**, and **Trend Breakout**) in two modes: **All-In** and **Scaled Positioning**. Rather than focusing solely on maximizing profit, my primary objective was to explore how strategies behave under different market conditions, manage risk, and maintain capital.

## ⚙️ Tech Stack

- **Language**: Python 3.10+
- **Data Source**: Real-time historical OHLCV from Binance via `ccxt`
- **Backtesting Framework**: Custom simulator with state management and stop-loss logic
- **Visualization**: Matplotlib for comparative analysis and drawdown monitoring

## 🗂️ Project Structure

- `simulate.py` — runs all simulations and writes output files
- `visualize.py` — generates comparison, breakdown, and drawdown plots
- `core/`
  - `data_fetcher.py` — fetches and saves BTC/USDT data from Binance
  - `metrics.py` — computes performance metrics (growth, drawdown, signal count)
- `strategies/`
  - `mean_reversion.py` — logic for mean reversion strategy
  - `momentum.py` — logic for momentum strategy
  - `trend_breakout.py` — logic for trend breakout strategy
- `signals/` — stores generated strategy signals as `.csv`
- `output/` — stores simulation results and generated charts (`.csv` + `.png`)

## 🛠️ How to Run

To run the project, follow these steps:

```bash
# Make sure Python 3.10+ is installed and added to your PATH
# You can get it from https://www.python.org/downloads/

# Clone the repository
git clone https://github.com/RiazBhuiyan03/raven-quant-task.git
cd raven-quant-task

# Install dependencies (option 1 - recommended)
pip install -r requirements.txt

# Or install manually (option 2)
pip install pandas matplotlib ccxt

# Run the simulation script
python simulate.py

# Generate strategy comparison charts
python visualize.py
```

### Output structure:

- `signals/` → raw buy/sell signals per strategy (.csv)
- `output/` → simulation results & visual charts (.csv + .png)
