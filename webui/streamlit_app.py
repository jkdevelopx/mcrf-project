import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scanner_engine import run_scanner
import yfinance as yf

st.set_page_config(
    page_title="MCRF Stock Scanner",
    layout="wide"
)

st.title("📈 MCRF Stock Scanner — Top Momentum Picks")

st.write("ระบบสแกนหุ้นตาม Momentum / Consistency / Relative Strength / Factor Model")

# Sidebar
st.sidebar.header("Scanner Options")
top_n = st.sidebar.slider("จำนวนหุ้นที่ต้องการแสดง (Top N)", 3, 20, 10)

# Run scanner button
if st.sidebar.button("🚀 Run Scanner Now"):
    with st.spinner("กำลังสแกนหุ้น…"):
        df = run_scanner()

    st.success("สำเร็จ! ผลลัพธ์พร้อมแล้ว")
    st.subheader("ผลลัพธ์ Top Picks")

    # Rank + Color scale
    df_display = df.copy().head(top_n)
    df_display.index = range(1, len(df_display) + 1)

    st.dataframe(df_display.style.background_gradient(cmap='Blues'))

    # Chart section
    st.subheader("📊 Price Trend")

    selected = st.selectbox("เลือกหุ้นเพื่อแสดงกราฟ", df_display["ticker"])

    data = yf.download(selected, period="1y")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name=selected
    ))

    fig.update_layout(
        title=f"ราคาย้อนหลัง 1 ปี — {selected}",
        height=400,
        xaxis_title="Date",
        yaxis_title="Price"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("กดปุ่ม 'Run Scanner Now' เพื่อเริ่มสแกนหุ้น")
