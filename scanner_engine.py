from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import yfinance as yf
from scoring import score_stock

def fetch_one(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1y")
        if data.empty:
            return None
        score = score_stock(data)
        return {"ticker": ticker, "score": score}
    except:
        return None

def run_scan_parallel(universe):
    results = []

    with ThreadPoolExecutor(max_workers=20) as ex:
        for r in ex.map(fetch_one, universe):
            if r:
                results.append(r)

    return pd.DataFrame(results)
