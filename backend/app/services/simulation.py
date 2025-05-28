import pandas as pd

def run_simulation_logic(signals_df: pd.DataFrame, stop_loss_pct: float, take_profit_pct: float, risk_per_trade_pct: float):
    """
    Simulate trades given signals DataFrame and risk management params.
    Returns stats dict.
    """

    if signals_df.empty:
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "accuracy": 0,
            "net_gain_pct": 0,
            "equity_curve": []
        }

    # Example assumption: signals_df has columns:
    # 'gain_pct' - actual percentage gain/loss of the trade (after SL/TP applied)
    # 'direction' - 'bullish'/'bearish' or similar

    # Apply stop loss and take profit as boundaries on gain_pct
    # If gain_pct < -stop_loss_pct => capped loss at -stop_loss_pct
    # If gain_pct > take_profit_pct => capped gain at take_profit_pct

    def capped_gain(row):
        gain = row['gain_pct']
        if gain < -stop_loss_pct:
            return -stop_loss_pct
        elif gain > take_profit_pct:
            return take_profit_pct
        else:
            return gain

    signals_df['adjusted_gain_pct'] = signals_df.apply(capped_gain, axis=1)

    total_trades = len(signals_df)
    winning_trades = signals_df[signals_df['adjusted_gain_pct'] > 0].shape[0]
    accuracy = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

    # Calculate net gain % assuming risk_per_trade_pct % risk per trade on account balance
    # For simplicity, assume position size = risk_per_trade_pct of current equity
    # Equity starts at 100 (arbitrary units)

    equity = 100.0
    equity_curve = [equity]

    for gain_pct in signals_df['adjusted_gain_pct']:
        # Profit or loss = risk_per_trade_pct * gain_pct / 100 of current equity
        pnl = equity * (risk_per_trade_pct / 100) * (gain_pct / 100)
        equity += pnl
        equity_curve.append(equity)

    net_gain_pct = ((equity - 100) / 100) * 100  # % gain over starting equity

    # Format equity_curve to list of floats (optional rounding)
    equity_curve = [round(val, 4) for val in equity_curve]

    result = {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "accuracy": round(accuracy, 2),
        "net_gain_pct": round(net_gain_pct, 2),
        "equity_curve": equity_curve,
    }

    return result
