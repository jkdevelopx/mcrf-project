# webui/streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from ui_utils import read_top_from_db, read_scores_since, df_to_csv_bytes
from pathlib import Path
import time


st.set_page_config(page_title='MCRF Dashboard', layout='wide')


# --- UI: header ---
st.title('📊 MCRF — Ultimate Dashboard')
st.markdown('Structured logs + historical DB + interactive charts')


# Theme toggle (simple)
if 'theme' not in st.session_state:
st.session_state['theme'] = 'light'


col1, col2 = st.columns([3,1])
with col2:
if st.button('Toggle theme'):
st.session_state['theme'] = 'dark' if st.session_state['theme']=='light' else 'light'


# Controls
with st.sidebar:
st.header('Controls')
top_n = st.number_input('Top N', min_value=3, max_value=200, value=10)
refresh = st.button('Refresh Data')
ticker_filter = st.text_input('Filter ticker (comma separated)')
days = st.slider('History days for score timeline', min_value=7, max_value=365, value=90)
export = st.button('Export Top as CSV')


# Data
if refresh or 'last_loaded' not in st.session_state:
st.session_state['last_loaded'] = time.time()
top_df = read_top_from_db(limit=500)
st.session_state['top_df'] = top_df
else:
top_df = st.session_state.get('top_df', pd.DataFrame())


# Filter
if ticker_filter:
tickers = [t.strip().upper() for t in ticker_filter.split(',') if t.strip()]
top_df = top_df[top_df['ticker'].isin(tickers)]


# Main layout
st.subheader('Top Hits (most recent)')
if top_df.empty:
st.info('No data in DB. Run scanner to generate logs and then ingest.')
else:
display_df = top_df[['ts','ticker','score','message']].head(top_n)
st.dataframe(display_df, use_container_width=True)


if export:
csv_bytes = df_to_csv_bytes(display_df)
st.download_button('Download CSV', csv_bytes, file_name='mcrf_top.csv')


# Score timeline
st.subheader('Score Timeline')
score_df = read_scores_since(days)
if score_df.empty:
st.info('No historical scores found')
else:
# pivot for plotting top tickers
top_ticks = score_df['ticker'].value_counts().head(10).index.tolist()
plot_df = score_df[score_df['ticker'].isin(top_ticks)].copy()
plot_df['ts'] = pd.to_datetime(plot_df['ts'])
fig = px.line(plot_df, x='ts', y='score', color='ticker', markers=True)
st.plotly_chart(fig, use_container_width=True)


# Footer
st.caption('MCRF — Ultimate Dashboard. Logs are stored in logs/mcrf.log and archived to db/history.db')