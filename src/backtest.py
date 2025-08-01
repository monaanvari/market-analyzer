import numpy as np
import ctypes
import time

def run_backtest(df):
    # Generate trading signals: 1 for long, -1 for short
    df["Signal"] = np.where(df["MA_Short"] > df["MA_Long"], 1, 0)

    
    # Compute daily returns
    df["Returns"] = df["Close"].pct_change()
    
    # Strategy returns: yesterday's signal * today's return
    df["Strategy"] = df["Signal"].shift(1) * df["Returns"]
    df["Strategy"].fillna(0, inplace=True)

    strategy_array = df["Strategy"].values

    # Pure Python PnL (benchmark)
    start = time.time()
    cum_pnl_py = (1 + df["Strategy"]).cumprod()
    py_time = time.time() - start

    # Buy-and-Hold PnL baseline
    buyhold_pnl = (1 + df["Returns"]).cumprod()

    # C++ optimized PnL (benchmark)
    start = time.time()
    cum_pnl_cpp = run_cpp_pnl(strategy_array)
    cpp_time = time.time() - start

    # Compute Sharpe ratio
    sharpe = compute_sharpe(df["Strategy"])

    # Coordinates for scatter plot: last time index, final C++ PnL
    scatter_x = len(df) - 1
    scatter_y = cum_pnl_cpp

    print(f"Python runtime: {py_time:.6f} sec")
    print(f"C++ runtime:   {cpp_time:.6f} sec")
    print(f"Sharpe Ratio: {sharpe:.2f}")

    return {
        "cum_pnl_py": cum_pnl_py,
        "cum_pnl_cpp": cum_pnl_cpp,
        "buyhold_pnl": buyhold_pnl,
        "py_time": py_time,
        "cpp_time": cpp_time,
        "sharpe": sharpe,
        "scatter_x": scatter_x,
        "scatter_y": scatter_y
    }

def run_cpp_pnl(strategy_array):
    lib = ctypes.CDLL("./src/pnl_calc.so")
    lib.computePnLSeries.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_double)
    ]
    
    arr = (ctypes.c_double * len(strategy_array))(*strategy_array)
    result = (ctypes.c_double * len(strategy_array))()
    
    lib.computePnLSeries(arr, len(strategy_array), result)
    
    return np.array(result)


def compute_sharpe(returns, risk_free_rate=0.0):
    excess_returns = returns - risk_free_rate/252  # daily risk-free adjustment
    mean_return = excess_returns.mean()
    std_return = excess_returns.std()
    if std_return == 0:
        return 0.0
    sharpe_ratio = (mean_return / std_return) * np.sqrt(252)  # annualized
    return sharpe_ratio
