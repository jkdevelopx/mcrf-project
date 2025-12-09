# dashboard/app.py
import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "infra/mcrf_logs.db"

st.set_page_config(page_title="MCRF Dashboard", layout="wide")

st.title("📊 MCRF — Market Composite Ranking Framework Dashboard")

# Read logs
def load_logs():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM logs ORDER BY ts DESC LIMIT 5000", conn)
    conn.close()
    return df

df = load_logs()

# Sidebar
st.sidebar.header("Filters")
ticker_list = df["ticker"].unique().tolist()
selected_tickers = st.sidebar.multiselect("Choose tickers", ticker_list, default=[])

min_score = st.sidebar.slider("Minimum score", 0, 100, 0)

# Filter
filtered = df[(df["score"] >= min_score)]
if selected_tickers:
    filtered = filtered[filtered["ticker"].isin(selected_tickers)]

st.subheader("Top Recent Scores")
st.dataframe(filtered.sort_values("score", ascending=False).head(20))

# Chart
st.subheader("Score Trend Over Time")
if selected_tickers:
    for t in selected_tickers:
        line = df[df.ticker == t].sort_values("ts")
        st.line_chart(line[["ts", "score"]].set_index("ts"))
else:
    st.info("Select a ticker from sidebar to see chart.")
