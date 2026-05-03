import streamlit as st
import requests
import numpy as np

# =========================
# CONFIG
# =========================
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="AI IDS Dashboard",
    layout="centered"
)

st.title("🚀 Real-Time Intrusion Detection System (IDS)")
st.write("Enter feature values to detect network attack or normal traffic")

# =========================
# INPUT SECTION
# =========================
st.subheader("📥 Input Features")

num_features = st.number_input(
    "Number of Features",
    min_value=1,
    max_value=200,
    value=10
)

features = []

for i in range(num_features):
    val = st.number_input(f"Feature {i+1}", value=0.0)
    features.append(val)

# =========================
# PREDICT BUTTON
# =========================
if st.button("🔍 Detect Attack"):

    payload = {
        "features": features
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        st.subheader("📊 Result")

        if "error" in result:
            st.error(result["error"])

        else:
            st.write("### Status:")
            st.success(result["status"])

            st.write("### Confidence Score:")
            st.metric(
                label="Attack Probability",
                value=result["confidence_score"]
            )

            st.write("### Risk Level:")
            st.info(result["risk_level"])

            # Visual indicator
            st.progress(float(result["confidence_score"]))

    except Exception as e:
        st.error(f"API Error: {str(e)}")

# =========================
# INFO PANEL
# =========================
st.sidebar.title("ℹ System Info")
st.sidebar.write("Backend: FastAPI")
st.sidebar.write("Model: XGBoost + CatBoost")
st.sidebar.write("Type: Hybrid IDS")