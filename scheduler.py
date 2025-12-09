import schedule
import time
import pandas as pd

from run_scanner import run_scan
from notify.discord import send_discord
from config import DISCORD_WEBHOOK, ALERT_SCORE_THRESHOLD

def job():
    print("Running scheduled scan...")

    # load universe
    universe = pd.read_csv("data/universe_small.csv")["ticker"].tolist()

    # run scan
    out = run_scan(universe)

    # filter
    hits = out[out.score >= ALERT_SCORE_THRESHOLD]

    if hits.empty:
        message = "No high-score tickers found today."
    else:
        lines = [f"{row.ticker} — {row.score}" for row in hits.itertuples()]
        message = "🚨 MCRF Auto Scan — High Score Picks\n" + "\n".join(lines)

    # send discord
    send_discord(DISCORD_WEBHOOK, message)
    print("Scheduled job finished.\n")

# run at 09:00 every day
schedule.every().day.at("09:00").do(job)

print("Scheduler started... waiting for next run...")

while True:
    schedule.run_pending()
    time.sleep(1)
