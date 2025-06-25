import streamlit as st
import requests
from PIL import Image
import base64
from datetime import datetime

# 📸 Set background image
def set_bg_from_local_image(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

# 🌐 Page Setup
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="wide")
set_bg_from_local_image("images/background.jpg")

# 🎨 Style
st.markdown("""
    <style>
    .center-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
    }
    .weather-box, .forecast-box, .datetime-box {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
    }
    .input-box {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    .input-box input {
        color: black;
        font-weight: bold;
    }
    .stButton > button {
        background-color: red !important;
        color: white !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .weather-box {
        background-color: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(5px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)


# 🏷️ Title
st.markdown("<div class='center-title'>🌦️ Real-Time Weather Dashboard</div>", unsafe_allow_html=True)

# 📦 Input Section
with st.container():
    col1, col2 = st.columns([2, 5])
    with col1:
        st.markdown("<div class='input-box'>", unsafe_allow_html=True)
        city = st.text_input("Enter City Name", key="city")
        if st.button("Get Weather"):
            st.session_state['fetch'] = True
        st.markdown("</div>", unsafe_allow_html=True)

# ✅ Main logic
if st.session_state.get("fetch") and city:
    api_key = "c867bca1a97af7bdbda50c412b5f204f"

    # 🌦️ Current Weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"]).strftime('%I:%M %p')
        sunset = datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"]).strftime('%I:%M %p')

        # 🔮 Forecast
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json() if forecast_response.status_code == 200 else {"list": []}

        # 🕒 Date & Time
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_day = now.strftime("%A, %d %B")

        # 📍 Row 1
        colA, colB = st.columns([1, 2])
        with colA:
            st.markdown(f"""
                <div class='datetime-box' style='text-align:center;'>
                    <h2>{city.title()}</h2>
                    <h1>{current_time}</h1>
                    <p>{current_day}</p>
                </div>
            """, unsafe_allow_html=True)

        with colB:
            st.markdown(f"""
                <div class='weather-box'>
                    <h3 style='text-align:center;'>🌍 Weather in {city.title()}</h3>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='flex: 1;'>
                            <p style='font-size: 30px;'>🌡️ {temp}°C</p>
                            <p style='font-size: 20px;'>💧 Humidity: {humidity}%</p>
                            <p style='font-size: 20px;'>💨 Wind: {wind} m/s</p>
                            <p style='font-size: 20px;'>🌤️ {desc.title()}</p>
                            <p style='font-size: 18px;'>🌅 {sunrise} | 🌇 {sunset}</p>
                        </div>
                        <div style='flex: 1; text-align: center;'>
                            <img src="{icon_url}" width="150">
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        

        
        # 📍 Row 2
        colC, colD = st.columns([3, 2])
        with colC:
            st.markdown("<div class='forecast-box'><h4 style='text-align:center;'>📅 3-Day Forecast</h4>", unsafe_allow_html=True)
            count = 0
            for entry in forecast_data["list"]:
                if "12:00:00" in entry["dt_txt"]:
                    date = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%A, %d %b")
                    forecast_temp = entry["main"]["temp"]
                    forecast_desc = entry["weather"][0]["description"].title()
                    icon_code = entry["weather"][0]["icon"]
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    st.markdown(f"""
                        <div style='margin-bottom:10px; display:flex; align-items:center;'>
                            <img src="{icon_url}" width="50" style="margin-right:10px;">
                            <b>{date}</b>: {forecast_temp}°C - {forecast_desc}
                        </div>
                    """, unsafe_allow_html=True)
                    count += 1
                    if count == 3:
                        break
            st.markdown("</div>", unsafe_allow_html=True)

        with colD:
            st.markdown(f"""
                <div class='datetime-box' style='text-align:center;'>
                    <h4>🌐 Current Date & Time</h4>
                    <h2>{current_time}</h2>
                    <p>{current_day}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("City not found. Please try again.")
