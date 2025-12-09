import json
import sqlite3
from pathlib import Path

LOG_DIR = Path("data/logs")
DB_PATH = "data/logs.db"

def ingest():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # สร้างตารางถ้ายังไม่มี
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT,
            ticker TEXT,
            score REAL,
            source TEXT
        )
    """)

    # อ่านทุกไฟล์ .jsonl ในโฟลเดอร์ data/logs
    for file in LOG_DIR.glob("*.jsonl"):
        print(f"Processing {file}")
        with open(file, "r") as f:
            for line in f:
                try:
                    obj = json.loads(line)

                    cur.execute("""
                        INSERT INTO logs (ts, ticker, score, source)
                        VALUES (?, ?, ?, ?)
                    """, (
                        obj.get("timestamp"),
                        obj.get("ticker"),
                        obj.get("score"),
                        obj.get("source", None)
                    ))

                except Exception as e:
                    print("Error parsing line:", e, line)

    conn.commit()
    conn.close()
    print("Ingestion completed!")

if __name__ == "__main__":
    ingest()
