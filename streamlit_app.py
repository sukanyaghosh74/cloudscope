# streamlit_app.py
import streamlit as st
import pandas as pd
import os
from src.forecast import forecast_cost
from src.anomaly_detector import detect_anomalies
import pygwalker as pyg

st.set_page_config(page_title="CloudScope", layout="wide")
st.title("☁️ CloudScope - Unified Cloud Cost Analyzer")

# Upload Section
st.sidebar.header("📤 Upload Cloud Billing Files")
uploaded_files = st.sidebar.file_uploader("Upload CSV(s) from AWS, Azure, GCP", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)

    st.success(f"✅ Uploaded {len(uploaded_files)} file(s). Merged shape: {merged_df.shape}")

    # Pygwalker Visualization
    st.subheader("📊 Interactive Exploration with Pygwalker")
    pyg_html = pyg.walk(merged_df, return_html=True)
    st.components.v1.html(pyg_html, height=800, scrolling=True)

    # Forecasting
    st.subheader("📈 Forecasting")
    try:
        forecast = forecast_cost(merged_df)
        st.metric(label="💸 Forecast Cost (Next 30 days)", value=f"${forecast:.2f}")
    except Exception as e:
        st.error(f"Error in forecasting: {e}")

    # Anomaly Detection
    st.subheader("🚨 Cost Anomaly Detection")
    try:
        anomalies = detect_anomalies(merged_df)
        if anomalies.empty:
            st.success("No anomalies detected ✅")
        else:
            st.dataframe(anomalies)
    except Exception as e:
        st.error(f"Error in anomaly detection: {e}")
else:
    st.info("Please upload at least one cloud billing CSV file to begin.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, Pygwalker, and love for cloud optimization.")
