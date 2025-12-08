# core/utils.py
import pandas as pd
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('mcrf')

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(subset=['Close'])
    df['Volume'] = df['Volume'].fillna(0)
    df = df[df['Volume'] > 0]
    return df

def chunk_list(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

def pick_top(df_scores, k=7):
    if df_scores is None or df_scores.empty:
        return df_scores
    return df_scores.sort_values('score', ascending=False).head(k)

def now_ts():
    return time.strftime('%Y-%m-%d %H:%M:%S')
