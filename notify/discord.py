# notify/discord.py
import requests
from config import DISCORD_WEBHOOK

def send_discord(message: str, webhook_url: str = None) -> bool:
    url = webhook_url or DISCORD_WEBHOOK
    if not url:
        print("No Discord webhook configured.")
        return False
    payload = {"content": message}
    try:
        r = requests.post(url, json=payload, timeout=8)
        r.raise_for_status()
        # Discord returns 204 No Content on success
        return True
    except Exception as e:
        print("Discord send failed:", e)
        return False
