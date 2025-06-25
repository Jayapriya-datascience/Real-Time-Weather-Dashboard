import streamlit as st
import requests
from PIL import Image
import datetime
import base64
from datetime import datetime


def set_bg_from_local_image(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Page setup
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️")

st.title("🌦️ Real-Time Weather Dashboard")
st.write("Enter a city name to see the current weather data.")

# Input field
city = st.text_input("Enter city name")

# Add this line to remove extra spaces
city = city.strip()

# API key
api_key = "c867bca1a97af7bdbda50c412b5f204f"

# ✅ Call the background function
set_bg_from_local_image("images/background.jpg")

st.markdown("""
<style>
div.stButton > button {
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: black !important;
    font-weight: bold !important;
    border: 1px solid black !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
}
</style>
""", unsafe_allow_html=True)


# 🎨 Style for input boxes and metric visibility
st.markdown("""
<style>
/* Weather Result: st.success */
section[data-testid="stNotification"] {
    color: black !important;
    background-color: rgba(0, 0, 0, 0.5) !important;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px;
}

/* Metric text (values like temp, humidity) */
div[data-testid="stMetricValue"] {
    color: white !important;
}

/* Metric label (title like "Temperature") */
div[data-testid="stMetricLabel"] {
    color: white !important;
}

/* Info box (like condition) */
div[data-testid="stMarkdownContainer"] p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* Make almost all visible text white */
html, body, .stApp, .stText, .stMarkdown, .stTitle, .stHeader, .stSubheader, .stMetric {
    color: white!important;
}

/* Input box text and placeholder */
input, textarea {
    color: black !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}
input::placeholder {
    color: #ddd !important;
}

/* Buttons */
button {
    color: black !important;
    background-color: rgba(255,255,255,0.9) !important;
}

/* Metric boxes */
.css-1v0mbdj, .stMetric {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 10px;
    color: black !important;
}

/* Optional: overlay for better readability */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.2);  /* subtle dark overlay */
    z-index: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* 🎯 Red Get Weather Button */
div.stButton > button {
    background-color: red !important;
    color: white !important;
    font-weight: bold !important;
    border: 2px solid darkred !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)





# 🌦️ Main logic
if st.button("Get Weather"):
    if city:
        city = city.strip()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            desc = data["weather"][0]["description"]
            
            # ✅ Sunrise & Sunset time extraction
            sunrise_ts = data["sys"]["sunrise"]
            sunset_ts = data["sys"]["sunset"]
            timezone_offset = data["timezone"]
            
            # Convert to readable local time
            sunrise_time = datetime.utcfromtimestamp(sunrise_ts + timezone_offset).strftime('%I:%M %p')
            sunset_time = datetime.utcfromtimestamp(sunset_ts + timezone_offset).strftime('%I:%M %p')

            st.markdown(f"""
            <div style='
                background-color: rgba(0,255,0,0.15); 
                color: black; 
                padding: 10px; 
                border-radius: 10px;
                font-weight: bold;
            '>
            🌍 Weather in {city.title()}
            </div>
            """, unsafe_allow_html=True)

            st.metric("🌡️ Temperature (°C)", temp)
            st.metric("💧 Humidity (%)", humidity)
            st.metric("💨 Wind Speed (m/s)", wind)

            
            # ✅ Display sunrise and sunset
            st.markdown(f"""
                <div style='margin-top: 10px; padding: 10px; border-radius: 10px;
                            background-color: rgba(255, 255, 255, 0.1); color: white;'>
                    🌅 <b>Sunrise:</b> {sunrise_time} &nbsp;&nbsp;&nbsp;
                    🌇 <b>Sunset:</b> {sunset_time}
                </div>
            """, unsafe_allow_html=True)
            st.info(f"🌤️ Condition: {desc.title()}")
            # 🔮 Fetch 3-day forecast (every 3 hours, we pick 12:00 PM entries)
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            forecast_response = requests.get(forecast_url)
            
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                st.subheader("📅 3-Day Forecast")
            
                count = 0
                for entry in forecast_data["list"]:
                    # Pick 12:00 PM entries only
                    if "12:00:00" in entry["dt_txt"]:
                        date = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%A, %d %b")
                        forecast_temp = entry["main"]["temp"]
                        forecast_desc = entry["weather"][0]["description"].title()
                        forecast_icon = entry["weather"][0]["icon"]
                        icon_url = f"http://openweathermap.org/img/wn/{forecast_icon}@2x.png"
            
                        # 🌤️ Display nicely
                        st.markdown(f"""
                            <div style='margin-bottom: 10px; padding: 10px; border-radius: 10px;
                                        background-color: rgba(255, 255, 255, 0.1); color: white;
                                        display: flex; align-items: center;'>
                                <img src="{icon_url}" width="50" style="margin-right:10px;">
                                <div>
                                    <b>{date}</b><br>
                                    🌡️ {forecast_temp} °C - {forecast_desc}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            
                        count += 1
                        if count == 3:
                            break
            else:
                st.warning("Couldn't fetch forecast data.")


        else:
            st.error(f"City not found. Status code: {response.status_code}")
    else:
        st.warning("Please enter a city name.")