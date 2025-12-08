# core/scoring.py
import numpy as np

def score(df, fundamentals: dict = None):
    if df is None or df.empty:
        return -999.0
    if fundamentals is None:
        fundamentals = {}

    last = df.iloc[-1]

    # defensive checks
    try:
        mom21 = float(last.get('Close') / df['Close'].shift(21).iloc[-1] - 1)
    except Exception:
        mom21 = 0.0
    rsi14 = float(last.get('RSI14', 50))
    vol_spike = float(last.get('Vol_Spike', 1))
    macd = float(last.get('MACD', 0)) - float(last.get('MACD_SIGNAL', 0))

    # Normalized signals
    mom_s = np.tanh(mom21 * 4)
    rsi_s = 1 - abs((rsi14 - 55) / 55)
    vol_s = np.tanh((vol_spike - 1.0) * 1)
    macd_s = np.tanh(macd * 3)

    # Fundamentals
    rev = fundamentals.get("revenueGrowth", 0) or 0
    rev_s = np.tanh(rev * 4)

    composite = (
        mom_s * 0.30 +
        rsi_s * 0.18 +
        vol_s * 0.18 +
        macd_s * 0.18 +
        rev_s * 0.16
    )

    score_val = (composite + 1) / 2 * 100
    return round(float(score_val), 2)
