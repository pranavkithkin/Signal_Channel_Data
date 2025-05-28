import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def optimize_strategy(
    df,
    sl_values=[1, 1.5, 2, 2.5, 3],
    tp_values=[3, 4.5, 5, 6, 7],
    risk_per_trade=0.01,
    initial_balance=1000,
    output_dir="simulations"
):
    """
    Run SL/TP optimization on the given DataFrame.
    Saves equity curves and a heatmap to output_dir.
    Returns a DataFrame with results for each SL/TP combination.
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for sl in sl_values:
        for tp in tp_values:
            balance = initial_balance
            equity_curve = []

            for _, row in df.iterrows():
                drawdown = abs(row.get('drawdown_pct', 0))
                direction = str(row.get('direction', '')).lower()
                gain_pct = None

                if direction == "bullish":
                    if drawdown >= sl:
                        gain_pct = -sl
                    elif row.get('gain_pct', 0) >= tp:
                        gain_pct = tp
                    else:
                        gain_pct = row.get('gain_pct', 0)
                elif direction == "bearish":
                    if drawdown >= sl:
                        gain_pct = -sl
                    elif row.get('gain_pct', 0) >= tp:
                        gain_pct = tp
                    else:
                        gain_pct = row.get('gain_pct', 0)
                else:
                    continue  # skip unrecognized

                profit = balance * risk_per_trade * (gain_pct / 100)
                balance += profit
                equity_curve.append(balance)

            gain = balance - initial_balance
            percent_return = (gain / initial_balance) * 100
            results.append({
                'SL%': sl,
                'TP%': tp,
                'Final Balance': round(balance, 2),
                'Total Return %': round(percent_return, 2)
            })

            # Save equity curve chart
            plt.figure(figsize=(10, 4))
            plt.plot(equity_curve, label=f'SL: {sl}% | TP: {tp}%', color='blue')
            plt.title(f'Equity Curve - SL: {sl}% | TP: {tp}%')
            plt.xlabel("Trades")
            plt.ylabel("Equity ($)")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/equity_SL{sl}_TP{tp}.png")
            plt.close()

    # Convert to DataFrame
    result_df = pd.DataFrame(results).sort_values(by="Final Balance", ascending=False)
    result_df.to_csv(f"{output_dir}/strategy_summary.csv", index=False)

    # Plot heatmap
    heatmap_data = result_df.pivot(index="SL%", columns="TP%", values="Total Return %")
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title("Total Return % (Final Equity) - SL vs TP")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/sl_tp_heatmap.png")
    plt.close()

    print(f"✅ Optimization complete. Results saved to {output_dir}")
    return result_df

# Optional: Allow running as a script
if __name__ == "__main__":
    # Example usage: python optimize_strategy.py
    df = pd.read_csv("backtest_results.csv")
    optimize_strategy(df)