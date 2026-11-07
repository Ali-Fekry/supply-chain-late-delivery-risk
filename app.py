from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "late_delivery_pipeline.joblib"
OPTIONS_PATH = ROOT / "models" / "app_options.json"
METADATA_PATH = ROOT / "models" / "model_metadata.json"

st.set_page_config(page_title="Supply Chain Late-Delivery Risk", page_icon="📦", layout="wide")
st.title("📦 Supply-Chain Late-Delivery Risk Checker")
st.caption("Estimate delivery risk from information available when an order is placed.")

if not all(path.exists() for path in (MODEL_PATH, OPTIONS_PATH, METADATA_PATH)):
    st.error("The trained model artifacts are missing. Check the models/ directory.")
    st.stop()

@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    options = json.loads(OPTIONS_PATH.read_text(encoding="utf-8"))
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return model, options, metadata

model, options, metadata = load_artifacts()
threshold = float(metadata.get("decision_threshold", 0.5))
schedule_mapping = options.get("scheduled_days_by_shipping_mode", {})

st.subheader("Order details")
left, right = st.columns(2)
with left:
    market = st.selectbox("Market", options.get("Market", []))
    shipping_mode = st.selectbox("Shipping mode", options.get("Shipping Mode", []))
with right:
    product = st.selectbox("Product", options.get("Product Name", []))
    scheduled_days = int(schedule_mapping.get(shipping_mode, 0))
    st.number_input("Scheduled shipping days", min_value=0, max_value=7, value=scheduled_days,
                    step=1, disabled=True,
                    help="Automatically set from the observed DataCo shipping-mode relationship.")

st.caption("Scheduled days are derived from the selected shipping mode to avoid unsupported combinations.")
if st.button("Estimate late-delivery risk", type="primary", use_container_width=True):
    order = pd.DataFrame([{
        "Market": market,
        "Shipping Mode": shipping_mode,
        "Product Name": product,
        "Days for shipment (scheduled)": scheduled_days,
    }])
    probability = float(model.predict_proba(order)[0, 1])
    predicted_late = probability >= threshold
    st.divider()
    st.subheader("Prediction")
    score_col, action_col = st.columns([1, 2])
    with score_col:
        st.metric("Estimated late-delivery probability", f"{probability:.1%}")
        st.progress(min(max(probability, 0.0), 1.0))
    with action_col:
        if predicted_late:
            st.warning("Higher late-delivery risk")
            st.markdown("**Suggested action:** Flag this order for operations review. Check carrier capacity and whether a faster option is feasible.")
        else:
            st.success("Lower late-delivery risk")
            st.markdown("**Suggested action:** Continue with the planned shipping mode and monitor normally.")
    st.caption(f"Decision threshold: {threshold:.0%}. This is a model estimate, not a delivery guarantee.")

with st.expander("About this model and its limitations"):
    st.write("Trained on DataCo Smart Supply Chain data using Market, Shipping Mode, Product Name, and scheduled shipping days.")
    st.write("Actual shipping duration, delivery status, actual shipping dates, and other post-outcome fields are excluded to prevent target leakage.")
    st.write("Evaluation groups all item rows from an Order Id together. Historical patterns may not represent current carrier or route conditions. Use the score for human review, not automatic shipping decisions.")
