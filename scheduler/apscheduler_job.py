import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from notify.discord import send_discord
from run_scanner import run_scan   # ใช้ของจริงจาก run_scanner.py
from config import ALERT_SCORE_THRESHOLD

def run_scan_job():
    """
    ฟังก์ชันสำหรับ APScheduler เพื่อรันสแกนอัตโนมัติ
    """
    print("Running scheduled scan...")

    # โหลด universe
    universe = pd.read_csv("data/universe_small.csv")["ticker"].tolist()

    # เรียกฟังก์ชันสแกนตัวจริง
    result = run_scan(universe)

    # เลือกหุ้นที่ score >= threshold
    hits = result[result.score >= ALERT_SCORE_THRESHOLD]

    if hits.empty:
        message = "No high-score tickers found today."
    else:
        lines = [f"{row.ticker} — {row.score}" for row in hits.itertuples()]
        message = "🚨 MCRF Auto Scan — High Score Picks\n" + "\n".join(lines)

    send_discord(message)
    print("Scheduled scan finished.")

def start_scheduler():
    scheduler = BlockingScheduler()
    # รันทุกวันตอน 9 โมงเช้า (local)
    scheduler.add_job(run_scan_job, "cron", hour=9, minute=0)
    print("Scheduler started — job scheduled.")
    scheduler.start()
