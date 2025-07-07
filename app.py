import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="AI KPI Dashboard", layout="wide")

st.title("🤖 AI Team KPI Dashboard")
st.subheader("📊 Мок-данные по команде NLP / MLOps / DevOps")

# Фейковые данные
dates = pd.date_range(start="2025-06-01", periods=30, freq="D")
data = pd.DataFrame({
    "date": dates,
    "precision": np.random.uniform(0.8, 0.97, size=30),
    "recall": np.random.uniform(0.75, 0.95, size=30),
    "latency_ms": np.random.randint(200, 800, size=30),
    "ci_cd_success_rate": np.random.uniform(0.8, 1.0, size=30),
    "uptime": np.random.uniform(99.5, 100.0, size=30),
    "nps": np.random.uniform(30, 90, size=30),
})

# KPI-графики
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📌 Precision & Recall (NLP)")
    chart = alt.Chart(data).transform_fold(
        ['precision', 'recall']
    ).mark_line().encode(
        x='date:T',
        y='value:Q',
        color='key:N'
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.markdown("### ⚡ Latency (ms)")
    st.line_chart(data.set_index("date")["latency_ms"])

st.markdown("### 🚀 CI/CD Success Rate")
st.line_chart(data.set_index("date")["ci_cd_success_rate"])

st.markdown("### ☁️ Uptime")
st.line_chart(data.set_index("date")["uptime"])

st.markdown("### ❤️‍🔥 NPS пользователей")
st.line_chart(data.set_index("date")["nps"])
