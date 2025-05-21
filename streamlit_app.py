import streamlit as st
import pandas as pd
import os
from src.main import normalize_uploaded_file
from src.anomaly_detector import detect_anomalies
from src.forecast import forecast_next_month
import pygwalker as pyg

st.set_page_config(page_title="CloudScope", layout="wide")
st.title("??? CloudScope - Unified Cloud Cost Analyzer")

st.sidebar.header("Upload Billing CSV")
provider = st.sidebar.selectbox("Select Cloud Provider", ["AWS", "Azure", "GCP"])
uploaded_file = st.sidebar.file_uploader("Upload your cost CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = normalize_uploaded_file(df, provider)

    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.dataframe(df)

    df = detect_anomalies(df)
    forecast = forecast_next_month(df)
    st.metric(label="?? Forecast Cost (Next 30 days)", value=f"\")

    st.subheader("?? Visual Explorer")
    pyg_html = pyg.to_html(df)
    st.components.v1.html(pyg_html, height=800, scrolling=True)

else:
    st.info("Please upload a CSV file to begin.")
