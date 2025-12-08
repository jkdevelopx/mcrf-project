# core/fetcher_batch.py
"""
Batch fetcher — combines multiple tickers into efficient batched pulls
for faster scanning & reduced API overhead.
"""
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from core.utils import clean_df
from core.indicators import compute_indicators

def fetch_one(ticker: str, period="1y", interval="1d"):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period, interval=interval, actions=False)
        if df is None or df.empty:
            return ticker, pd.DataFrame()
        df = df[["Open","High","Low","Close","Volume"]].copy()
        df.index = pd.to_datetime(df.index)
        return ticker, df
    except Exception:
        return ticker, pd.DataFrame()

def batch_fetch(tickers, period="1y", interval="1d", max_workers=12):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = [ex.submit(fetch_one, t, period, interval) for t in tickers]
        for f in futs:
            t, df = f.result()
            results[t] = df
    return results

def batch_prepare(tickers, period="1y", interval="1d", max_workers=12):
    raw = batch_fetch(tickers, period, interval, max_workers)
    final = {}
    for t, df in raw.items():
        if df is None or df.empty:
            final[t] = pd.DataFrame()
            continue
        df = clean_df(df)
        df = compute_indicators(df)
        final[t] = df
    return final
