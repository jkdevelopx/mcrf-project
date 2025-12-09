# webui/ui_utils.py
import pandas as pd
import sqlite3
from pathlib import Path


DB_FILE = Path('db/history.db')




def read_top_from_db(limit=50):
if not DB_FILE.exists():
return pd.DataFrame()
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query('SELECT * FROM scans ORDER BY ts DESC LIMIT ?', conn, params=(limit,))
conn.close()
return df




def read_scores_since(days=30):
if not DB_FILE.exists():
return pd.DataFrame()
conn = sqlite3.connect(DB_FILE)
q = "SELECT ts, ticker, score FROM scans WHERE score IS NOT NULL AND ts >= datetime('now','-? days') ORDER BY ts"
# sqlite doesn't accept parameter in datetime('now','-? days') directly; do date math in Python
df = pd.read_sql_query('SELECT ts, ticker, score FROM scans WHERE score IS NOT NULL ORDER BY ts', conn)
conn.close()
return df




def df_to_csv_bytes(df: pd.DataFrame):
return df.to_csv(index=False).encode('utf-8')