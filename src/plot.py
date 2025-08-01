def plot_results(df, results):
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10,5))
    plt.plot(results["cum_pnl_py"], label="Strategy PnL (Python)", color="blue")
    plt.plot(results["buyhold_pnl"], label="Buy & Hold", color="green", linestyle="--")
    
    # Add scatter point for final C++ PnL
    plt.plot(df.index, results["cum_pnl_cpp"], label="Strategy PnL (C++)", color="red", linestyle=":")

    plt.title("Moving Average Strategy vs Buy & Hold")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Returns")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()
