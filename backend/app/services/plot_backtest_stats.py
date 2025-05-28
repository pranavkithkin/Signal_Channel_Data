import pandas as pd

def get_equity_curve_data(df, capital=1000, risk_per_trade=0.01):
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values("timestamp")
    equity = [capital]
    for gain in df['gain_pct']:
        last = equity[-1]
        pnl = last * risk_per_trade * (gain / 100)
        equity.append(last + pnl)
    df['equity'] = equity[1:]
    return {
        "timestamps": df['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
        "equity": df['equity'].tolist()
    }

def get_win_loss_data(df):
    win_count = (df['direction'].str.lower() == 'bullish').sum()
    loss_count = (df['direction'].str.lower() == 'bearish').sum()
    return {'Buy Setup': int(win_count), 'Sell setup': int(loss_count)}

def get_gain_distribution_data(df):
    if 'gain_pct' not in df.columns:
        return []
    return df['gain_pct'].dropna().tolist()

def get_drawdown_distribution_data(df):
    if 'drawdown_pct' not in df.columns or 'coin' not in df.columns:
        return {"coins": [], "drawdowns": []}
    df = df.dropna(subset=['drawdown_pct', 'coin'])
    return {
        "coins": df['coin'].tolist(),
        "drawdowns": df['drawdown_pct'].tolist()
    }

def get_coin_performance_data(df):
    perf = df.groupby('coin')['gain_pct'].mean().sort_values()
    return {
        "coins": perf.index.tolist(),
        "avg_gain": perf.values.tolist()
    }