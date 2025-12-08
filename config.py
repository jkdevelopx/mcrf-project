# config.py — clean & production-safe
import os
import sys


def env(name: str, default=None, cast=str):
    """Helper: read env vars with type casting + default"""
    val = os.environ.get(name, default)
    try:
        return cast(val)
    except:
        print(f"[CONFIG] Bad value for {name}: {val}")
        return cast(default)


# ------------- WEBHOOK (must be provided manually) -------------
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK')
if not DISCORD_WEBHOOK:
    print("[WARN] DISCORD_WEBHOOK is not set. Discord alerts disabled.")


# ------------- SCANNER SETTINGS -------------
ALERT_SCORE_THRESHOLD = env("ALERT_SCORE_THRESHOLD", 80, float)
FETCH_PERIOD_DAYS     = env("FETCH_PERIOD_DAYS", 365, int)
BATCH_SIZE            = env("BATCH_SIZE", 50, int)


# ------------- SCHEDULER -------------
ENABLE_SCHEDULER = env("ENABLE_SCHEDULER", "false", str).lower() in ("true","1","yes")

