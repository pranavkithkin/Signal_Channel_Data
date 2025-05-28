import pandas as pd

# Load signal + price data
df = pd.read_csv("signals_with_price_data.csv")

# Backtest config
risk_reward = 3.0        # 1:3 RR
risk_pct = 0.05          # 5% stop-loss (relative to entry)
results = []

for _, row in df.iterrows():
    direction = row['direction']
    entry = row['entry_price']
    high = row['future_high']
    low = row['future_low']
    coin = row['coin']
    timestamp = row['timestamp']

    sl = tp = outcome = drawdown_pct = gain_pct = None

    if direction == "Bullish":
        sl = entry * (1 - risk_pct)
        tp = entry * (1 + risk_pct * risk_reward)

        if low <= sl:
            outcome = "SL"
            gain_pct = -risk_pct * 100
        elif high >= tp:
            outcome = "TP"
            gain_pct = risk_pct * risk_reward * 100
        else:
            outcome = "None"
            gain_pct = ((high - entry) / entry) * 100

        drawdown_pct = ((entry - low) / entry) * 100

    elif direction == "Bearish":
        sl = entry * (1 + risk_pct)
        tp = entry * (1 - risk_pct * risk_reward)

        if high >= sl:
            outcome = "SL"
            gain_pct = -risk_pct * 100
        elif low <= tp:
            outcome = "TP"
            gain_pct = risk_pct * risk_reward * 100
        else:
            outcome = "None"
            gain_pct = ((entry - low) / entry) * 100

        drawdown_pct = ((high - entry) / entry) * 100

    results.append({
        "timestamp": timestamp,
        "coin": coin,
        "direction": direction,
        "entry_price": entry,
        "TP_price": tp,
        "SL_price": sl,
        "gain_pct": round(gain_pct, 2),
        "drawdown_pct": round(drawdown_pct, 2),
        "outcome": outcome,
        "raw_message": row["raw_message"]
    })

result_df = pd.DataFrame(results)
result_df.to_csv("backtest_results.csv", index=False)

# Print summary
win_rate = (result_df['outcome'] == 'TP').mean() * 100
loss_rate = (result_df['outcome'] == 'SL').mean() * 100
undecided = (result_df['outcome'] == 'None').mean() * 100
avg_gain = result_df['gain_pct'].mean()
max_gain = result_df['gain_pct'].max()
min_gain = result_df['gain_pct'].min()
avg_drawdown = result_df['drawdown_pct'].mean()

print(f"\n✅ Backtest Summary:")
print(f"Win Rate (TP): {win_rate:.2f}%")
print(f"Loss Rate (SL): {loss_rate:.2f}%")
print(f"No Decision (neither TP nor SL): {undecided:.2f}%")
print(f"Avg % Gain: {avg_gain:.2f}%, Max: {max_gain:.2f}%, Min: {min_gain:.2f}%")
print(f"Avg Drawdown Before TP: {avg_drawdown:.2f}%")
