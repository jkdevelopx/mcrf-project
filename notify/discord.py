# notify/discord.py
import requests

def send_discord(webhook_url: str, message: str):
    """
    ส่งข้อความไปที่ Discord webhook
    """
    payload = {"content": message}
    try:
        r = requests.post(webhook_url, json=payload)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[Discord] Error: {e}")
        return False
