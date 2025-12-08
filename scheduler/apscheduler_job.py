# scheduler/apscheduler_job.py
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from core.fetcher import fetch_history
from core.indicators import add_basic_indicators
from core.scoring import score_signals
from core.utils import chunk_list, log
from notify.discord import send_discord_alert
from config import BATCH_SIZE, FETCH_PERIOD_DAYS, ALERT_SCORE_THRESHOLD
import pandas as pd


# load universe
uni = pd.read_csv('data/universe_small.csv')['ticker'].astype(str).tolist()


sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=24)
def daily_scan_job():
log.info('Starting daily scan')
hits = []
for batch in chunk_list(uni, BATCH_SIZE):
for t in batch:
df = fetch_history(t, period_days=FETCH_PERIOD_DAYS)
if df is None:
continue
df = add_basic_indicators(df)
score = score_signals(df)
if score >= float(ALERT_SCORE_THRESHOLD):
hits.append((t, score))
# optional: short sleep to avoid rate limit
if hits:
body = 'MCRF Daily Hits:\n' + '\n'.join([f"{t} — {s}" for t,s in hits])
send_discord_alert(body)
log.info('Daily scan done')


if __name__ == '__main__':
sched.start()