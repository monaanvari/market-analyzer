
# Market Analyzer: Moving Average Backtester with Python & C++

## Overview
This project implements and benchmarks a **moving average crossover trading strategy** using both Python and C++ for performance comparison.  
It compares the strategy against a **buy-and-hold baseline** and evaluates key performance metrics such as **Sharpe ratio** and **cumulative returns**.  
The Python portion handles data processing and plotting, while C++ is used for optimized profit-and-loss (PnL) calculations.

---

## Features
- Fetches and preprocesses historical market data.
- Implements a **moving average crossover strategy**:
  - Long when short MA > long MA.
  - Neutral otherwise.
- Calculates daily returns, cumulative PnL, and risk metrics.
- Benchmarks **Python vs C++ performance** for PnL calculation.
- Visualizes:
  - Strategy PnL (Python).
  - Buy & Hold baseline.
  - Strategy PnL (C++).
- Computes risk-adjusted returns via **Sharpe ratio**.

---

## Project Structure
```

market-analyzer/
│
├── data/
│   └── Data.xlsx          # Historical data input
│
├── src/
│   ├── analyze.py         # Main script to run backtest & plot
│   ├── backtest.py        # Backtesting logic
│   ├── plot.py            # Plotting utilities
│   └── pnl_calc.cpp       # C++ PnL calculation
│
└── README.md              # Project documentation

````

---

## How It Works

### 1. Data Preprocessing
```python
df["MA_Short"] = df["Close"].rolling(20).mean()
df["MA_Long"] = df["Close"].rolling(50).mean()
````

* Short-term (20-day) and long-term (50-day) moving averages are computed.
* A signal is generated: `1` (long) if short MA > long MA, else `0`.

### 2. Strategy & Returns

```python
df["Strategy"] = df["Signal"].shift(1) * df["Returns"]
```

* Returns are shifted to avoid lookahead bias.
* The strategy is always long or neutral.

### 3. Performance Metrics

* **Cumulative Returns**: `(1 + returns).cumprod()`
* **Sharpe Ratio**: risk-adjusted return, annualized.
* **Max Drawdown** (optional extension): largest peak-to-trough loss.

### 4. C++ Integration

PnL is computed in C++ for speed:

```cpp
void computePnLSeries(double* strategy, int n, double* result) {
    result[0] = 1.0;
    for (int i = 1; i < n; i++) {
        result[i] = result[i-1] * (1.0 + strategy[i]);
    }
}
```

Bound to Python via `ctypes`.

### 5. Visualization

* Blue: Strategy PnL (Python).
* Green dashed: Buy & Hold.
* Red dotted: Strategy PnL (C++).

---

## Example Output

```
Python runtime: 0.000080 sec
C++ runtime:   0.000949 sec
Sharpe Ratio: 0.46
```

![Example Plot](./docs/example_plot.png)

---

## Requirements

* Python 3.10+
* Packages:

  * `pandas`
  * `numpy`
  * `matplotlib`
  * `yfinance`
  * `openpyxl`
* C++ compiler (e.g., `g++`).

---

## Run the Project

1. Install dependencies:

```bash
pip install pandas numpy matplotlib yfinance openpyxl 
```

2. Compile C++ library:

```bash
g++ -shared -o src/pnl_calc.so -fPIC src/pnl_calc.cpp
```

3. Run analysis:

```bash
python src/analyze.py
```

---

## Next Steps / Improvements

* Add **max drawdown** to risk metrics.
* Extend to multiple tickers for robustness testing.
* Add trade costs (commissions/slippage).
* Explore other strategies (e.g., RSI, Bollinger Bands).
* Optimize further with vectorized NumPy or Numba.

---

## Notes
* This project demonstrates the **workflow of designing, testing, and evaluating** a trading strategy — not necessarily producing a profitable one.

