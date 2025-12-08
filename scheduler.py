import schedule
import time
from datetime import datetime

from scanner_engine import run_scanner
from notify_discord import send_discord_message
from log_config import setup_logging
from config import DISCORD_WEBHOOK, SCHEDULE_TIME, LOG_FILE

logger = setup_logging(LOG_FILE)


def job():
    logger.info("Running MCRF scheduled job...")

    try:
        df = run_scanner()
        logger.info("Scanner completed")

        top_hits = df.head(5)

        msg = "**📈 MCRF — Daily Top Hits**\n"
        msg += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        for _, r in top_hits.iterrows():
            msg += f"• **{r['ticker']}** — Score: `{r['score']:.2f}`\n"

        send_discord_message(DISCORD_WEBHOOK, msg)
        logger.info("Discord message sent")

    except Exception as e:
        logger.error(f"Error in job: {e}")
        send_discord_message(DISCORD_WEBHOOK, f"❌ Scanner Error: {e}")


def start_scheduler():
    logger.info(f"Scheduler started. Running daily at {SCHEDULE_TIME}")
    schedule.every().day.at(SCHEDULE_TIME).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()
