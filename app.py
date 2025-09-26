import streamlit as st
import pickle
import numpy as np
import pandas as pd
from weather_fetcher import get_weather
from PIL import Image
import tensorflow as tf
import os
import gdown

st.set_page_config(page_title="AgroSense 🌾", layout="centered")

# --------------------------
# Custom CSS
# --------------------------
def add_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1510844355160-2fb07bf9af75?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-attachment: fixed;
        }
        section.main > div { display: flex; justify-content: center; align-items: center; height: 100vh; }
        section.main > div > div { background-color: rgba(0,0,0,0.5); padding: 2rem; border-radius: 12px; max-width: 850px; }
        section.main h1, section.main h2, section.main h3, section.main h4, section.main h5, section.main h6, section.main p, section.main span, section.main div { color: #ffffff !important; }
        [data-testid="stSidebar"] { background-color: #f5f6f8; }
        [data-testid="stSidebar"] * { color: #000000 !important; }
        button[kind="primary"] { background-color: #ffffff !important; color: black !important; border: 2px solid #999 !important; border-radius: 8px !important; font-weight: 600; padding: 0.4rem 1rem !important; transition: all 0.3s ease; }
        button[kind="primary"]:hover { background-color: #e6e6e6 !important; transform: scale(1.03); }
        .stSelectbox div[data-baseweb="select"] { color: black !important; }
        .stSelectbox label { color: white !important; }
        </style>
    """, unsafe_allow_html=True)

add_custom_css()

st.title("🌾 AgroSense - AI Powered Agricultural Assistant")
st.markdown("Welcome to AgroSense! Please select a module from the sidebar.")

# --------------------------
# Google Drive links
# --------------------------
MODELS_DIR = "models"
ARTIFACTS_DIR = "artifacts/disease"

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

CROP_MODEL_URL = "https://drive.google.com/uc?id=1FVcyWGiLzmxPanqzbyqG7ALbHLccybqZ"  
DISEASE_MODEL_URL = "https://drive.google.com/uc?id=1hKQ0gPgWHKkQJ4cpoKfIOuePlZGuNIhu"  

# --------------------------
# Download function
# --------------------------
def download_file_if_missing(url, output_path):
    if not os.path.exists(output_path):
        gdown.download(url, output_path, quiet=False, use_cookies=False)

# --------------------------
# Download models
# --------------------------
download_file_if_missing(CROP_MODEL_URL, os.path.join(MODELS_DIR, "crop_model.pkl"))
download_file_if_missing(DISEASE_MODEL_URL, os.path.join(ARTIFACTS_DIR, "plant_disease_model.h5"))

# --------------------------
# Sidebar menu
# --------------------------
menu = ["Home", "Crop Recommendation", "Fertilizer Suggestion", "Weather Info","Disease Detection"]
choice = st.sidebar.selectbox("Select Module", menu)

# --------------------------
# Home
# --------------------------
if choice == "Home":
    st.subheader("📌 About This App")
    st.write("""
    AgroSense is a smart decision-support system for farmers. It offers:
    - ✅ Crop recommendation using soil data
    - ✅ Fertilizer suggestions
    - ✅ Real-time weather insights
    - ✅ Disease detection via leaf image
    """)

# --------------------------
# Crop Recommendation
# --------------------------
elif choice == "Crop Recommendation":
    st.subheader("🌱 Crop Recommendation System")
    st.markdown("Enter the following soil and environmental conditions:")

    N = st.number_input("Nitrogen (N)", 0, 140, step=1)
    P = st.number_input("Phosphorous (P)", 5, 145, step=1)
    K = st.number_input("Potassium (K)", 5, 205, step=1)
    temperature = st.number_input("Temperature (°C)", 0.0, 50.0, step=0.1)
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, step=0.1)
    ph = st.number_input("pH value", 0.0, 14.0, step=0.1)
    rainfall = st.number_input("Moisture / Rainfall (mm)", 0.0, 300.0, step=0.1)

    if st.button("🔍 Recommend Crop"):
        try:
            with open(os.path.join(MODELS_DIR, "crop_model.pkl"), "rb") as f:
                model = pickle.load(f)
            input_data = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                                      columns=['N','P','K','temperature','humidity','ph','rainfall'])
            prediction = model.predict(input_data)[0]
            st.success(f"✅ Recommended Crop: **{prediction.title()}**")
        except Exception as e:
            st.error(f"❌ Error occurred: {e}")

# --------------------------
# Weather Info
# --------------------------
elif choice == "Weather Info":
    st.subheader("☁️ Real-time Weather Info")
    city = st.text_input("Enter your city name", "Hyderabad")
    if st.button("🌦️ Get Weather"):
        weather = get_weather(city)
        if isinstance(weather, str):
            st.error(f"❌ Error: {weather}")
        else:
            st.success("✅ Weather fetched successfully!")
            st.markdown(f"**City:** {weather['city']}")
            st.markdown(f"**Temperature:** {weather['temperature']}°C")
            st.markdown(f"**Humidity:** {weather.get('humidity','N/A')}%")
            st.markdown(f"**Condition:** {weather['weather']}")
            if weather["temperature"] > 40:
                st.warning("🔥 Very hot! Consider drought-resistant crops.")
            elif weather["temperature"] < 15:
                st.warning("❄️ Too cold! Avoid sensitive crops.")
            if weather["humidity"] > 80:
                st.warning("💧 High humidity! Watch for fungal diseases.")

# --------------------------
# Fertilizer Suggestion
# --------------------------
elif choice == "Fertilizer Suggestion":
    st.subheader("💧 Fertilizer Suggestion System")
    crop_name = st.selectbox("Select Crop", sorted([
        'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
        'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
        'banana', 'mango', 'grapes', 'watermelon', 'muskmelon',
        'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'
    ]))
    N = st.number_input("Nitrogen (N)", 0, 140, step=1)
    P = st.number_input("Phosphorous (P)", 5, 145, step=1)
    K = st.number_input("Potassium (K)", 5, 205, step=1)
    if st.button("📤 Suggest Fertilizer"):
        try:
            from fertilizer_suggestion import suggest_fertilizer
            suggestion = suggest_fertilizer(crop_name.lower(), N, P, K)
            st.success("✅ Fertilizer Advice:")
            st.markdown(f"🧪 {suggestion}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --------------------------
# Disease Detection
# --------------------------
elif choice == "Disease Detection":
    st.subheader("🩺 Leaf Disease Detection")
    uploaded_file = st.file_uploader("📤 Upload a leaf image", type=["jpg","jpeg","png"])
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            image = image.resize((128,128))
            image_array = np.expand_dims(np.array(image)/255.0, axis=0)
            st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
            model = tf.keras.models.load_model(os.path.join(ARTIFACTS_DIR,"plant_disease_model.h5"))
            predictions = model.predict(image_array)
            predicted_class = np.argmax(predictions, axis=1)[0]
            class_names = [
                "Apple Scab","Apple Black Rot","Apple Cedar Rust","Apple Healthy",
                "Corn Gray Leaf Spot","Corn Common Rust","Corn Northern Leaf Blight","Corn Healthy",
                "Grape Black Rot","Grape Esca","Grape Leaf Blight","Grape Healthy",
                "Potato Early Blight","Potato Late Blight","Potato Healthy"
            ]
            st.success(f"✅ Detected Disease: **{class_names[predicted_class]}**")
        except Exception as e:
            st.error(f"❌ Error loading model or making prediction: {e}")
