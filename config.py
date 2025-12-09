# config.py — production-safe
import os

def env(name, default=None, cast=str):
    v = os.environ.get(name, default)
    try:
        return cast(v)
    except Exception:
        return default

DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK')  # must be set in env
if not DISCORD_WEBHOOK:
    print("[WARN] DISCORD_WEBHOOK is not set. Discord alerts disabled.")

ALERT_SCORE_THRESHOLD = env("ALERT_SCORE_THRESHOLD", 80, float)
FETCH_PERIOD_DAYS     = env("FETCH_PERIOD_DAYS", 365, int)
BATCH_SIZE            = env("BATCH_SIZE", 50, int)
ENABLE_SCHEDULER      = env("ENABLE_SCHEDULER", "false", str).lower() in ("true","1","yes")

# OpenAI (optional, for AI advisor)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
