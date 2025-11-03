import streamlit as st
import spacy
import pickle
import numpy as np

# Page config
st.set_page_config(page_title="Intent Classification App", layout="wide")

# Load models
nlp = spacy.load("en_core_web_lg")
model = pickle.load(open("svc_model.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))

def predict_intent(query):
    vec = nlp(query).vector.reshape(1, -1)
    pred_class = model.predict(vec)[0]
    pred_proba = model.predict_proba(vec).max()
    intent_label = le.inverse_transform([pred_class])[0]
    return intent_label, pred_proba

# ---- SIDEBAR INPUT ----
st.sidebar.header("💬 Enter Your Query")
query = st.sidebar.text_area("Type here...", "", height=120)
predict_btn = st.sidebar.button("Predict Intent")

# ---- MAIN LAYOUT ----
st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>Intent Classification System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Get the predicted intent and confidence for your queries</p>", unsafe_allow_html=True)
st.divider()

# ---- PREDICTION RESULT ----
if predict_btn:
    if query.strip():
        intent, conf = predict_intent(query)
        # Color coding confidence
        if conf > 0.8:
            bg_color = "#d4edda"  # green
        elif conf > 0.5:
            bg_color = "#fff3cd"  # yellow
        else:
            bg_color = "#f8d7da"  # red

        st.markdown(
            f"""
            <div style='background-color:{bg_color};padding:20px;border-radius:15px;box-shadow:2px 2px 10px rgba(0,0,0,0.1);margin-bottom:20px;'>
                <h2 style='color:#4B8BBE;'>Predicted Intent: {intent}</h2>
                <p style='font-size:18px;'>Confidence: <strong>{conf:.2f}</strong></p>
            </div>
            """, unsafe_allow_html=True
        )
        st.progress(conf)
    else:
        st.warning("⚠️ Please enter a query to predict.")

# ---- TEST EXAMPLES ----
st.subheader("📌 Test Examples")
examples = [
    "Set an alarm for 7 AM tomorrow",
    "Play some music",
    "Send a message to John",
    "What's the weather today?",
    "Turn on the flashlight"
]

for q in examples:
    intent, conf = predict_intent(q)
    if conf > 0.8:
        bg_color = "#d4edda"
    elif conf > 0.5:
        bg_color = "#fff3cd"
    else:
        bg_color = "#f8d7da"

    st.markdown(
        f"""
        <div style='background-color:{bg_color};padding:15px;border-radius:12px;margin-bottom:12px;box-shadow:1px 1px 5px rgba(0,0,0,0.1);'>
            <strong>Query:</strong> {q} <br>
            <strong>Intent:</strong> {intent} <br>
            <strong>Confidence:</strong> {conf:.2f}
        </div>
        """, unsafe_allow_html=True
    )

# ---- FOOTER ----
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Made with ❤️ using Streamlit & spaCy</p>", unsafe_allow_html=True)
