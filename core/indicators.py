# core/indicators.py
import pandas as pd
import numpy as np

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    df = df.copy()

    # --- Moving Averages ---
    df['MA20'] = df['Close'].rolling(20, min_periods=5).mean()
    df['MA50'] = df['Close'].rolling(50, min_periods=10).mean()
    df['MA200'] = df['Close'].rolling(200, min_periods=50).mean()

    # --- RSI ---
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / (roll_down + 1e-9)
    df['RSI14'] = 100 - (100 / (1 + rs))

    # --- Bollinger Bands ---
    df['BB_MID'] = df['Close'].rolling(20).mean()
    df['BB_STD'] = df['Close'].rolling(20).std()
    df['BB_UP'] = df['BB_MID'] + 2 * df['BB_STD']
    df['BB_LOW'] = df['BB_MID'] - 2 * df['BB_STD']

    # --- ATR ---
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = (df['High'] - df['Close'].shift(1)).abs()
    df['L-PC'] = (df['Low'] - df['Close'].shift(1)).abs()
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1)
    df['ATR14'] = df['TR'].rolling(14).mean()

    # --- MACD ---
    exp12 = df['Close'].ewm(span=12, adjust=False).mean()
    exp26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp12 - exp26
    df['MACD_SIGNAL'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # --- Volatility ---
    df['Volatility20'] = df['Close'].pct_change().rolling(20).std() * (252 ** 0.5)

    # --- Volume Spike ---
    df['Vol_MA20'] = df['Volume'].rolling(20).mean()
    df['Vol_Spike'] = df['Volume'] / (df['Vol_MA20'] + 1e-9)

    return df
