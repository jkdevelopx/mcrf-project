# run_scanner.py
from core.fetcher_batch import batch_prepare
from core.scoring import score
from core.utils import pick_top
import pandas as pd
import yfinance as yf
import os
from notify.discord import send_discord

# config via env or defaults
from config import DISCORD_WEBHOOK, FETCH_PERIOD_DAYS, BATCH_SIZE, ALERT_SCORE_THRESHOLD

def run_scan(tickers, period="1y"):
    data = batch_prepare(tickers, period=period, max_workers=12)
    results = []

    for t, df in data.items():
        try:
            info = {}
            try:
                info = yf.Ticker(t).info
            except Exception:
                info = {}
            s = score(df, info)
        except Exception:
            s = -999
        results.append({"ticker": t, "score": s})

    df_scores = pd.DataFrame(results)
    topk = pick_top(df_scores, k=7)
    return topk

if __name__ == "__main__":
    # basic manual runner
    import sys
    if len(sys.argv) > 1:
        tickers = sys.argv[1:]
    else:
        # fallback small universe
        tickers = pd.read_csv('data/universe_small.csv')['ticker'].astype(str).tolist()
    top = run_scan(tickers)
    print(top.to_string(index=False))
    # send discord if threshold matched
    hits = top[top['score'] >= float(ALERT_SCORE_THRESHOLD)]

if not hits.empty and os.environ.get('DISCORD_WEBHOOK'):
    lines = [f"{r.ticker} — {r.score}" for r in hits.itertuples()]
    body = "MCRF Top Hits:\n" + "\n".join(lines)
    send_discord(os.environ.get('DISCORD_WEBHOOK'), "MCRF Daily Hits", body)
