# core/fetcher.py
# Provides a thin abstraction over data providers.
import pandas as pd
from typing import Optional


# prefer yahooquery in restricted environments, fallback to yfinance
try:
from yahooquery import Ticker as YQ
PROVIDER = 'yahooquery'
except Exception:
import yfinance as yf
PROVIDER = 'yfinance'




def fetch_history(symbol: str, period_days: int = 365) -> Optional[pd.DataFrame]:
period_map = {30:'1mo',90:'3mo',180:'6mo',365:'1y',730:'2y'}
period = period_map.get(period_days, f"{period_days}d")
try:
if PROVIDER == 'yahooquery':
t = YQ(symbol)
df = t.history(period=period)
if df is None or df.empty:
return None
df = df.reset_index()
if 'symbol' in df.columns:
df = df[df['symbol'].str.upper()==symbol.upper()]
# normalize
colmap = {}
if 'date' in df.columns:
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
for k in ('open','high','low','close','volume'):
if k in df.columns:
colmap[k] = k.capitalize()
df = df.rename(columns=colmap)
expected = ['Open','High','Low','Close','Volume']
if not all(c in df.columns for c in expected):
return None
return df[expected]
else:
t = yf.Ticker(symbol)
df = t.history(period=period)
if df is None or df.empty:
return None
df = df[['Open','High','Low','Close','Volume']].copy()
df.index = pd.to_datetime(df.index)
return df
except Exception:
return None