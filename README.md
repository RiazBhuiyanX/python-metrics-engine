<h1 align="left">
  <img src="extras/raven_logo_256.png" alt="Logo" width="40" style="vertical-align: middle;"/>
  Raven Quant Task
</h1>

## 📚 Table of Contents

- [🧠 Summary](#-summary)
- [⚙️ Tech Stack](#%EF%B8%8F-tech-stack)
- [📂 Project Structure](#%EF%B8%8F-project-structure)
- [🛠️ How to Run](#️-how-to-run)
- [🧭 Strategy Exploration & Justification](#-strategy-exploration--justification)
- [📉 Risk Management & Capital Protection](#-risk-management--capital-protection)
- [🧪 Backtesting Engine Design](#-backtesting-engine-design)
- [📊 Metrics & Performance Interpretation](#-metrics--performance-interpretation)
- [📈 Strategy Performance Comparison: All-In vs Scaled](#-strategy-performance-comparison-all-in-vs-scaled)
- [📉 Drawdown Analysis & Risk Behavior](#-drawdown-analysis--risk-behavior)
- [🚀 What I’d Improve with More Time](#-what-id-improve-with-more-time)
- [🐞 Challenges & Bugs I Solved](#-challenges--bugs-i-solved)
- [🎯 Final Reflections](#-final-reflections)

## 🧠 Summary

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
```

### Output structure:

- `signals/` → raw buy/sell signals per strategy (.csv)
- `output/` → simulation results & visual charts (.csv + .png)

### 🔁 Pre-Generated Results Available

This repo already includes:

- Precomputed strategy signals in `/signals/*.csv`
- Final simulation results in `/output/*.csv`
- Visual charts for strategy comparison and drawdown in `/output/*.png`

You do **not** need to re-run the scripts unless you want to test live data again.

### 🧪 Want to Run on Fresh Data?

You can re-run the full pipeline on new Binance data by doing:

```bash
# Run the simulation script
python simulate.py

# Generate strategy comparison charts
python visualize.py
```

## 🧭 Strategy Exploration & Justification

When I first approached the challenge, I didn’t think of myself as a "trader" in the traditional sense. But I realized that I _do_ trade — just in a different context. My family runs a small business, and we often buy trending products and sell them at a premium. We try to anticipate demand, buy low, and sell high.

That mindset helped me frame this task in familiar terms: instead of predicting markets, I looked for **patterns where people tend to overreact**, and where we can **systematically profit** from that behavior while limiting the downside.

---

### 🔍 Reviewing Popular Strategies

To design something that could reasonably perform in a volatile, fee-less, short-term setting, I first explored a wide range of well-known trading approaches:

#### ❌ Rejected Strategies

| Strategy                 | Why I Didn't Use It                                                                                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Scalping**             | Requires ultra-low-latency execution and constant monitoring. Even though we assume zero fees, scalping relies on capturing small price inefficiencies — not feasible with OHLCV data and a basic simulator. |
| **Market Making**        | Too complex to simulate fairly. Market-making requires bid/ask spread modeling and order book interaction, which is out of scope here.                                                                       |
| **Arbitrage**            | Relies on inter-exchange latency and infrastructure. Not signal-based, and impossible to replicate in a static backtest.                                                                                     |
| **Swing/Day Trading**    | Describes time horizon, not entry/exit logic. My focus was on **strategy logic**, not holding duration.                                                                                                      |
| **Pure Trend Following** | Too vulnerable to false breakouts in sideways markets, which dominate low timeframes. I needed strategies that adapt faster.                                                                                 |

I also briefly explored the idea of **Market Making** (providing liquidity on both the buy and sell sides) and **Arbitrage** (covering all outcomes like in sports betting).
I quickly realized these strategies couldn't be tested fairly in this setup — market making requires a full order book simulation, and arbitrage isn't possible without multiple exchanges or pricing discrepancies to exploit.

---

### ✅ Strategy 1: Mean Reversion (initial choice)

After narrowing it down, **Mean Reversion** was my natural starting point:

- On short timeframes (5m), crypto prices often fluctuate around a local equilibrium.
- With **no fees**, even small reversion moves (~0.2%) can be captured profitably.
- It mirrors the behavior of a reactive market-maker — buying when others panic sell, and selling into spikes.
- It's conservative, which aligned with my initial mindset: **protect capital first**, then grow it.

This strategy laid the foundation for my simulator and metrics engine.

---

### ➕ Why I Added Momentum

While mean reversion works well in sideways or “choppy” markets, it **fails during strong trends** — exactly when you should _not_ bet against the direction.

So I added a **Momentum strategy**, which does the opposite:

- It enters **with the trend**, assuming that strong moves tend to persist.
- It uses SMA crossovers (short vs. long) to identify directionality shifts.
- It's simple, robust, and performs well in trending environments — especially during breakouts or directional moves.

By comparing it with Mean Reversion, I could test **how well a strategy performs _in regime X_ vs _regime Y_**.

---

### ➕ Why I Added Trend Breakout

Momentum helps catch trends _once they’ve formed_. But what if we want to catch **the breakout itself**?

That’s where the **Trend Breakout strategy** comes in:

- It enters long if price exceeds the highest high of the last N candles.
- It enters short if price drops below the lowest low.
- This strategy is **reactive to price action itself**, not just moving averages.

The goal here was to build a strategy that would **capture explosive moves** early — especially when volatility spikes.

It also allows for great comparison:

- Breakout = high volatility reaction
- Momentum = trend confirmation
- Mean Reversion = equilibrium pullback

---

### 📈 Why I Chose BTC/USDT

I selected the BTC/USDT pair for multiple practical and strategic reasons:

- **Liquidity**: BTC/USDT is one of the most liquid trading pairs in crypto, which means price movements are less distorted by individual trades. This makes backtests more reliable.
- **Volatility**: Bitcoin exhibits natural volatility on short timeframes — ideal for testing both breakout and mean-reversion logic.
- **Data Availability**: It’s easy to obtain clean, high-frequency OHLCV data from Binance using `ccxt`, with minimal missing values or anomalies.
- **Market Independence**: BTC is a decentralized asset not tied to company earnings or interest rates. This lets me test price-based strategies without needing to model macroeconomic factors.
- **USDT Stability**: Using USDT as the quote currency makes all balances stable and easy to interpret (i.e., gains/losses are not exposed to FX risk or inflation).

In short, BTC/USDT offers a dynamic, clean, and high-volume sandbox to experiment with strategy logic under realistic market conditions.

## 📉 Risk Management & Capital Protection

From the start, I treated this challenge not as a profit-maximization game, but as a **survival problem**. As the prompt says — if you lose 50%, you need 100% gain to recover. Capital preservation had to be baked into the logic.

### 🛑 Stop Logic: 80% Capital Threshold

I implemented a **hard stop-loss rule**: if total portfolio value dropped below 800 USDT (20% drawdown), trading would halt for that strategy run.

- This mimics a real-life trader going risk-off after significant losses.
- It also prevents "death spirals", especially in All-In mode.

This rule created a simple but effective **fail-safe** for high-risk setups.

### 🔀 Two Execution Modes: All-In vs Scaled

Each strategy was tested in two capital deployment styles:

| Mode       | Description                                                            | Pros                           | Cons                             |
| ---------- | ---------------------------------------------------------------------- | ------------------------------ | -------------------------------- |
| **All-In** | Full capital is used on every signal (buy or sell)                     | High return potential          | Very high drawdown risk          |
| **Scaled** | Gradual exposure: 95% of USDT used when buying, or only 5% of BTC sold | Lower volatility, smoother PnL | May underperform in strong moves |

#### 💡 Why 95% Buy / 5% Sell?

This ratio was not arbitrary — I chose it after observing how **BTC tends to climb gradually** over time. Here's the reasoning:

- **Buying with 95%** allows strong exposure to upside momentum without fully locking capital. It takes advantage of BTC's long-term uptrend while retaining 5% liquidity in USDT.
- **Selling only 5%** avoids full liquidation, preserving upside in case of false reversal signals.
- It smooths out volatility: profits accrue over multiple steps rather than hinging on one entry/exit.
- Empirically, this produced **higher final balances and lower drawdowns** across most strategies.

Overall, the 95/5 split offered a sweet spot: high enough exposure to catch profitable trends, but conservative enough to avoid full liquidation on choppy price action.

#### ⚠️ Minimum USDT Threshold

In the Scaled mode, I also added a practical rule: **no new buy trades are executed if available USDT falls below 10**.

This prevents:

- Executing irrelevant micro-trades that distort metrics
- Artificial capital depletion through many near-zero transactions
- Unrealistic results where rounding errors affect outcomes

This threshold reflects a real-world constraint: in actual markets, exchanges enforce minimum trade sizes, and capital efficiency matters. There's no point in spending your last $3 on a micro-trade if it can't meaningfully move your portfolio.

### 🧠 Risk Philosophy

In live markets, position sizing and risk control are often more important than the signal itself. I wanted my simulator to reflect that:

- No leverage
- No compounding
- No overtrading
- Simple, strict rules

This made the testing **more interpretable** and kept the focus on strategy behavior, not edge-case mechanics.

## 🧪 Backtesting Engine Design

To test each strategy fairly, I built a simple but consistent backtesting engine that models portfolio state over time. The goal wasn’t to create an industrial-grade simulator, but to capture the **essential dynamics** of trade execution, capital allocation, and risk control.

### 🧩 Core Concepts

- **State Tracking**: At every candle, the simulator tracks:

  - USDT balance
  - BTC holdings
  - Total portfolio value
  - Active signal (1 = buy, -1 = sell, 0 = hold)
  - Whether the stop condition has been triggered

- **Signal Execution**:

  - If signal = `1` (buy):
    - **All-In**: use all USDT to buy BTC
    - **Scaled**: use 95% of USDT if above 10
  - If signal = `-1` (sell):
    - **All-In**: sell all BTC
    - **Scaled**: sell 5% of BTC balance

- **Stop Logic**:

  - If total portfolio drops below 800 USDT, stop is triggered.
  - All further signals are ignored for that run.

- **Final Metrics**:
  - Growth %
  - Max drawdown %
  - Signal count
  - Duration of simulation
  - Final balance

### 💾 Output Logging

Each simulation writes to a `.csv` file with full trade-by-trade data:

- `timestamp`, `price`, `signal`, balances, total value, stop trigger

This makes it easy to:

- Visualize progress over time
- Compare strategies side-by-side
- Debug or audit the logic

---

### ⚠️ Known Limitations

This engine makes a few **deliberate simplifications**:

- Assumes **instant execution at close price** of each candle
- No slippage or partial fills
- No position fees (per instructions)
- No latency between signal and trade

These choices make the logic **transparent and deterministic**, which helps focus on strategy behavior without microstructure noise.

## 📊 Metrics & Performance Interpretation

Once each simulation completes, I compute several key performance metrics using the final portfolio history. These metrics help me evaluate how each strategy behaves — not just whether it made money, but how it handled risk and signal efficiency.

### 📈 What I Measure

| Metric                  | Description                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| **Growth %**            | Final total USDT balance relative to starting capital            |
| **Max Drawdown %**      | Worst peak-to-trough drop in total balance during the simulation |
| **Buy/Sell Signals**    | Total number of actionable signals                               |
| **Simulation Duration** | Time between first and last candle                               |

These are calculated via the `metrics.py` module after each run.

### 📊 How I Interpret Results

A good strategy isn’t just one with the **highest final balance**, but one that also manages capital **with acceptable drawdowns and consistent logic**. For example:

- A high-growth strategy with huge drawdowns may be too risky in real-world trading.
- A low-signal strategy with modest profit might be more attractive if it's stable and repeatable.
- Scaled versions often had **smoother equity curves** and **better capital preservation**, especially in sideways or volatile markets.

By comparing All-In vs Scaled for each strategy, I gained insight into **how capital deployment affects strategy robustness**.

### 🧪 Sample Insight

> In my tests, Trend Breakout (All-In) had a higher peak balance, but also the steepest drawdown. Its Scaled variant offered better consistency, especially during choppy markets where breakouts often failed.

These kinds of contrasts helped me reason about **when and why** to use a particular strategy or risk mode.

### 🧱 Realistic Constraints

Not every Buy/Sell signal leads to a trade.

- If the portfolio holds no USDT (in All-In), a Buy signal is skipped.
- If BTC holdings are zero (in Scaled or All-In), Sell signals are ignored.
- These edge cases are common in real trading and affect signal count vs execution count.

Also, I deliberately did **not** compute advanced metrics like:

- **Sharpe Ratio**
- **Win Rate**
- **CAGR / Annualized Return**

Why? Because the simulation spans only **~3 days and 11 hours** (1000 x 5-minute candles). Metrics like Sharpe or annualized return are misleading or unstable on such short periods.

I didn’t want to include stats that would **inflate precision but reduce realism**.

## 📈 Strategy Performance Comparison: All-In vs Scaled

Below is a breakdown of how each strategy performed in both All-In and Scaled modes. Each pair of curves reveals important dynamics in risk, return, and stability.

---

### 🔁 Mean Reversion

<img src="output/breakdown_mean_reversion.png" alt="Mean Reversion"/>

**Final Balance:**

- All-In: **1053.80 USDT**
- Scaled: **1068.13 USDT**

**Observations:**

- Scaled clearly outperformed, both in terms of final return and smoothness.
- All-In mode exhibits stair-step jumps with long flat periods — this indicates capital was fully deployed and unable to act on further signals.
- Scaled took advantage of smaller pullbacks more frequently, maintaining exposure and reacting quickly.
- Drawdowns in Scaled mode were less severe and recovered faster.

**Conclusion:**  
Mean Reversion works best when it can react often. Scaled mode enables that flexibility, while All-In "locks" the capital and causes missed opportunities.

---

### 📈 Momentum

<img src="output/breakdown_momentum.png" alt="Momentum"/>

**Final Balance:**

- All-In: **1052.63 USDT**
- Scaled: **1059.10 USDT**

**Observations:**

- Both modes tracked similarly until mid-simulation, after which Scaled shows more stability and smoother gains.
- All-In experienced more frequent drawdowns due to whipsaws (false momentum shifts).
- Scaled mode appears more resilient — it benefited from staying partially in the market, instead of flipping entirely on each signal.

**Conclusion:**  
Momentum signals can be noisy. A Scaled approach smooths out the effects of false moves, creating a more robust equity curve.

---

### 💥 Trend Breakout

<img src="output/breakdown_trend_breakout.png" alt="Trend Breakout"/>

**Final Balance:**

- All-In: **1037.87 USDT**
- Scaled: **1060.71 USDT**

**Observations:**

- This is the most dramatic difference between modes.
- All-In was hurt by failed breakouts — after buying in fully, prices reversed quickly, causing extended losses.
- Scaled mode stayed reactive and nimble, preserving capital through partial exits and entries.
- The breakout logic is more volatile by nature, and Scaled mode acts as a volatility buffer.

**Conclusion:**  
For breakout strategies, capital preservation is key. Scaled mode significantly reduced damage from false signals and helped capture late-stage moves.

## 🏆 Full Strategy Showdown: All Variants Compared

The plot below compares the full equity curves of all six strategy-mode combinations:

- **Mean Reversion (All-In & Scaled)**
- **Momentum (All-In & Scaled)**
- **Trend Breakout (All-In & Scaled)**

<img src="output/strategy_comparison.png" alt="All strategies"/>

This view helps answer one question:  
**Which strategy, in which mode, handled this specific market window best?**

---

### 🥇 Top Performer

📈 **Mean Reversion (Scaled)** achieved the **highest final balance (1068.13 USDT)** with the **smoothest equity curve**. It captured many small pullbacks and avoided major drawdowns.

---

### 🥈 Strong Contenders

- **Trend Breakout (Scaled)**: Final balance of 1060.71 USDT. Volatile at times, but managed to recover and stay strong in the final stretch.
- **Momentum (Scaled)**: 1059.10 USDT. Consistent growth, though slightly affected by whipsaws.

All **Scaled modes** outperformed their All-In counterparts — highlighting the importance of capital management.

---

### 🚨 Weaker Performers

- **Trend Breakout (All-In)**: The worst performer at 1037.87 USDT. Suffered from multiple failed breakouts and lacked re-entry flexibility.
- **Momentum (All-In)** and **Mean Reversion (All-In)** had similar outcomes (~1052–1053 USDT), but showed more drawdown and plateaus due to capital lock-in.

---

### 💡 Final Insight

This comparison reinforces a key idea:

> **The signal logic matters — but how you size your positions and manage your exposure matters just as much.**

Scaled strategies allowed smoother PnL, faster recovery from losses, and more adaptability to uncertain price action.

### 📉 Why Mean Reversion Outperformed

Even though BTC was in a mild uptrend during the simulation period, **Mean Reversion (Scaled)** delivered the best performance. This may seem counterintuitive at first — trend-following strategies should benefit most from upward moves.

However, several factors explain this outcome:

- The trend was not clean or sustained — it included frequent short-term pullbacks.
- These conditions are ideal for **mean reversion**, which exploits temporary price deviations.
- On the 5-minute timeframe, breakouts were often false or reversed quickly.
- Scaled mean reversion allowed the portfolio to stay active and responsive without overcommitting capital.
- Momentum and breakout strategies, on the other hand, suffered more from signal lag and whipsaws.

This highlights the fact that **direction alone is not enough** — the _structure_ and _volatility profile_ of the market matters just as much.

### 📊 Summary Table

| Strategy       | Mode   | Final Balance | Notes                            |
| -------------- | ------ | ------------- | -------------------------------- |
| Mean Reversion | All-In | 1053.80       | Missed smaller entries, choppy   |
|                | Scaled | 1068.13       | Best performer, smooth growth    |
| Momentum       | All-In | 1052.63       | Sharp drawdowns on false trends  |
|                | Scaled | 1059.10       | More resilient to whipsaws       |
| Breakout       | All-In | 1037.87       | Exposed to failed breakouts      |
|                | Scaled | 1060.71       | Smoothed damage, captured trends |

### 🧠 A Note on Data Limitations

While these results offer useful insights into how each strategy behaves under my test setup, I fully acknowledge the **limited scope of the data**:

- The simulation covers only **~3.5 days** of 5-minute candles (1000 data points).
- During this period, **BTC was in a mild uptrend**, which naturally favors long-biased strategies like momentum and breakout.
- A sideways or strongly bearish market would likely shift the relative performance of these strategies — possibly favoring mean reversion or reducing profitability altogether.

My conclusions are therefore **conditional**, not universal. These tests validate structure and execution flow, but **not long-term edge**.

Given more time and data, I would test the strategies across:

- Different volatility regimes
- Bearish vs bullish trends
- Extended historical windows (e.g., several weeks or months)

This would allow for more statistically robust results and help distinguish between strategies that are **structurally sound** and those that are just **lucky over a short stretch**.

## 📉 Drawdown Analysis & Risk Behavior

Profit is not the only metric that matters — **drawdown** shows how much capital is at risk during downturns. Below is the **maximum drawdown %** for each strategy-mode combination:

| Strategy       | Mode   | Max Drawdown % |
| -------------- | ------ | -------------- |
| Mean Reversion | All-In | -1.03%         |
|                | Scaled | -1.61%         |
| Momentum       | All-In | -1.82%         |
|                | Scaled | -1.97%         |
| Breakout       | All-In | -2.68%         |
|                | Scaled | -1.91%         |

---

### 🧠 Why Scaled ≠ Always Lower Drawdown

One might expect **Scaled** versions to always reduce drawdown — but in my case, that wasn’t always true. Here’s why:

#### 🔸 1. **Slower Execution Accumulation**

In Scaled mode, positions are built gradually. This means exposure increases _after_ the signal, not instantly. If the price moves against the position during accumulation, losses compound over time.

#### 🔸 2. **Prolonged Partial Holding**

Unlike All-In (which exits fully), Scaled mode reduces position size slowly. This can **prolong time in drawdown**, especially in volatile chop.

#### 🔸 3. **Short Duration Simulation**

With only ~3.5 days of data, **short-term volatility has a disproportionate impact**. One or two unlucky entries in Scaled mode may skew drawdown without enough time to recover.

---

### 📉 Visual Breakdown

Below are drawdown-over-time plots for each All-In strategy. These help illustrate how “painful” each path is for a trader.

#### 🔁 Mean Reversion (All-In)

<img src="output/drawdown_mean_reversion_all-in.png" alt="Mean Reversion"/>

#### ⚡ Momentum (All-In)

<img src="output/drawdown_momentum_all-in.png" alt="Momentum"/>

#### 💥 Trend Breakout (All-In)

<img src="output/drawdown_trend_breakout_all-in.png" alt="Trend Breakout"/>

As shown, Trend Breakout All-In had the deepest and most persistent drawdowns, consistent with its overall poor performance. Mean Reversion and Momentum had shallower but more frequent drops — a sign of noisy signals and fast reactivity.

---

### 🔍 Final Insight

> **Risk isn't just numbers — it's what you have to emotionally survive.**

A strategy with a -1.8% drawdown might look better than one with -2.6%, but if it hits that number more often, or recovers slower, it may feel riskier in practice.

Drawdown curves help tell the _real story_ behind the PnL line.

## 🚀 What I’d Improve with More Time

While the current implementation fulfills the goal of exploring strategy behavior and risk, it operates within tight constraints: only ~3.5 days of historical data, no slippage, no latency, and simplified assumptions. Here's what I would expand or refine with more time:

---

### 1. Broader & Longer Data Horizon

- The simulation uses only **1000 candles of 5-minute data**, or about 3.5 days.
- I would fetch **several weeks to months** of data and test across **different market regimes** (bullish, bearish, ranging).
- This would allow me to evaluate **statistical robustness**, **overfitting sensitivity**, and **stability across volatility profiles**.

---

### 2. Smarter Risk Management Models

- Current logic uses fixed % thresholds (e.g., 95% buy, 5% sell, 80% stop).
- With more time, I’d implement:
  - **Volatility-based sizing** (e.g. standard deviation)
  - **Trailing stop losses**
  - **Dynamic exposure adjustment** based on drawdown or recent signal accuracy
- This would help create more adaptable strategies that can self-correct under stress.

---

### 3. Strategy Combination & Regime Detection

- Currently, strategies run independently.
- I’d build a simple **regime classifier** (trend, range, volatility burst), and **dynamically allocate capital** to the most suitable strategy at any point.
- This would mimic a realistic portfolio that pivots based on market behavior.

---

### 4. Advanced Performance Metrics

- I deliberately skipped metrics like **Sharpe Ratio**, **CAGR**, **Win Rate**, and **Profit Factor**, because the current dataset is too short to yield meaningful values.
- With more data, I would compute:
  - **Sharpe** for risk-adjusted return
  - **Win Rate** to evaluate signal quality
  - **CAGR** to estimate long-term growth potential
  - **Max consecutive losses** to understand emotional tolerance

---

### 5. Execution & Microstructure Modeling

- Right now, the simulator assumes perfect execution at close price.
- A more realistic engine would include:
  - **Slippage**
  - **Partial fills**
  - **Latency between signal and execution**
  - **Minimum order size filters**
- These would help evaluate which strategies are robust in practice, not just in theory.

---

### 6. Better Visualization & Real-Time Monitoring

- I would improve plots with interactive drill-down, zoom, and overlayed indicators.
- Ideally, I’d also add a **real-time dashboard** that streams live strategy behavior during simulation (Plotly, Streamlit, etc.)

---

### 7. Walk-Forward Testing & Cross-Validation

- The current approach tests strategies on one contiguous time block.
- I would implement:
  - **Walk-forward validation** to simulate real deployment
  - **Rolling-window re-evaluation**
  - Possibly even **cross-validation folds** for parameter robustness (e.g., SMA windows)

---

### 📦 Final Thought

This challenge helped me focus on **clarity over complexity**, and to prioritize **capital preservation, interpretability, and reactivity**. With more time, I’d go deeper in market modeling — but even in this limited context, I believe the design choices demonstrate a deliberate and structured approach to trading system design.

## 🐞 Challenges & Bugs I Solved

Building this project wasn't a straight line — it took a lot of trial, error, and iteration. Below are some real-world issues I encountered and resolved along the way:

---

### 1. Timeframe Confusion & Too-Short Testing Windows

I originally started with **1-minute candles**, testing a simple **Mean Reversion strategy** using a ±0.5% threshold and an All-In execution model. That gave me only about **3 hours of market activity**, which quickly felt unrealistic.  
The results were noisy and unstable — too few trades, too fast dynamics, and very little actionable insight.

After testing multiple configurations, I eventually **settled on 5-minute candles with 1000 bars (~3.5 days)**, which offered a good balance between noise reduction and signal density.

---

### 2. Parameter Tuning by Observation, Not Overfitting

My initial 0.5% threshold was too wide for short-term candles — the strategy barely traded.  
Through experimentation, I found that **0.2% worked better** for capturing micro-deviations, especially on the 5-minute timeframe.

I also realized that I didn’t need to look back 20 candles at 1m resolution — I could look at just **10 candles of 5m**, reducing computation while keeping the same market scope.

---

### 3. Designing the Scaled Execution Mode

Initially, I only had an All-In model. But it quickly became clear that this was too binary and rigid — once capital was deployed, it couldn’t respond to new signals.

I implemented a **Scaled Mode** (95% buy / 5% sell), but this also introduced edge cases — like when the USDT balance was under 10. I had to explicitly prevent micro-trades that distorted results and made no practical sense.

---

### 4. Rounding Bug That Broke Trade Logic

At one point, I was rounding values **before checking trade conditions**, which led to logic errors where trades were skipped even though enough capital existed.  
It took a while to notice that I was essentially discarding valid trades due to premature rounding.

Fixing this small bug improved trade accuracy and signal alignment across runs.

---

### 5. Overoptimistic Metrics Early On

In early versions, I calculated metrics like CAGR and Sharpe as if I was running over **a full year** — which made every strategy look amazing on paper.  
But that was misleading: the test window was only 3.5 days.

I rewrote the metrics logic to reflect only the **actual simulation duration**, making the results much more realistic and honest.

---

### ✅ Final Thoughts

None of these were "big showstopper" bugs — but together, they shaped the final quality and credibility of the project. I treated each issue not just as a fix, but as a learning opportunity to make the framework more robust and realistic.

In the end, what you're seeing is the result of **dozens of small course corrections** — and that process was honestly the most valuable part.

## 🎯 Final Reflections

Coming into this challenge, I had never written or traded a real algorithmic strategy before. My only reference point was how we run our physical store — where we try to buy trending items before others, and sell them at a premium.  
That mindset helped me approach the markets in a way that felt intuitive: **find patterns, manage inventory (capital), and survive volatility.**

---

I didn’t try to “beat the market” with fancy indicators or aggressive curve fitting. Instead, I focused on:

- Building clear, interpretable strategies
- Managing risk carefully
- Making honest assumptions
- And learning from every failed test

Along the way, I encountered bugs, bad metrics, unrealistic assumptions, and edge cases I hadn’t planned for — and every one of them taught me something new.

---

More than anything, this project gave me a deeper appreciation for how **fragile trading strategies can be**, and how much value there is in simplicity, clarity, and robustness.

Whether or not my code was perfect, I’m proud of how I approached the problem: like a real-world trader would — with curiosity, discipline, and a healthy respect for uncertainty.

## 📎 Appendix & Project Info

### 📄 License

This project is provided for educational purposes only under the MIT License.

### 🙏 Acknowledgements

Thanks to the Raven team for designing such an open-ended and intellectually rewarding challenge.  
And a special nod to the Discord community — reading others' struggles and progress kept me motivated and focused.

### ⚠️ Disclaimer

This project is a simulation intended for academic and evaluation purposes only.  
It does not constitute financial advice or a recommendation to trade.  
Past performance is not indicative of future results.

### 👤 Author

**Name:** Riaz Bhuiyan  
**GitHub:** [@RiazBhuiyan03](https://github.com/RiazBhuiyan03)
