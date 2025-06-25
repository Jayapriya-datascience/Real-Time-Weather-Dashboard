import streamlit as st
import requests
from PIL import Image
import base64
from datetime import datetime
import plotly.graph_objs as go


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
    col1, col2 = st.columns([5, 2])  # Wider input, smaller button

    with col1:
        city = st.text_input(label="", key="city", placeholder="Enter City Name")
        st.markdown("<style>input::placeholder { color: black; font-weight: bold; }</style>", unsafe_allow_html=True)


    with col2:
        st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
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
        feels_like = data["main"]["feels_like"] 
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
                    <h2 style='text-align:center;'>🌍 Weather in {city.title()}</h2>
                    <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                        <div style='flex: 1; text-align: center;'>
                            <img src="https://img.icons8.com/fluency/96/sunrise.png" width="60" style="margin-bottom: 5px;">
                            <p style='font-size: 16px; font-weight: bold; margin: 0; color: black;'>{sunrise}</p>
                            <div style="height: 10px;"></div>
                            <img src="https://img.icons8.com/color/96/sunset--v1.png" width="60" style="margin-bottom: 5px;">
                            <p style='font-size: 16px; font-weight: bold; margin: 0; color: black;'>{sunset}</p>
                        </div>
                        <div style='flex: 1;'>
                            <h2 style='font-size: 40px;'>🌡️ {temp}°C</h2>
                            <p style='text-align: center; color:black;'>Feels like: {feels_like}°C</p>
                            <p style='font-size: 18px; text-align: center;'>💧 Humidity: {humidity}%</p>
                            <p style='font-size: 18px; text-align: center;'>💨 Wind: {wind} m/s</p>
                        </div>
                        <div style='flex: 1; text-align: right;'>
                            <img src="{icon_url}" width="100" style="margin-top: 5px;">
                            <p style='font-size: 18px; font-weight: bold; color: black; margin-top: 3px;'>{desc.title()}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        
        # 📍 Row 2
        colC, colD = st.columns([3, 2])
        with colC:
            st.markdown("""
                <div class='forecast-box'>
                    <h3 style='text-align:center; margin-bottom: 10px;'>📅 3-Day Forecast</h3>
            """, unsafe_allow_html=True)
        
            count = 0
            for entry in forecast_data["list"]:
                if "12:00:00" in entry["dt_txt"]:
                    date = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%A, %d %b")
                    forecast_temp = entry["main"]["temp"]
                    forecast_desc = entry["weather"][0]["description"].title()
                    icon_code = entry["weather"][0]["icon"]
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
                    st.markdown(f"""
                        <div style='
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            background-color: rgba(255, 255, 255, 0.1);
                            padding: 10px;
                            margin-bottom: 10px;
                            border-radius: 5px;
                            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                        '>
                            <div style='flex: 1; font-weight: bold; font-size: 20px;'>{date}</div>
                            <div style='flex: 1; text-align: center;'>
                                <img src="{icon_url}" width="95" style="margin-top: -0px;">
                            </div>
                            <div style='flex: 2; font-size: 20px; text-align: right; font-weight: bold;'>
                                {forecast_temp}°C - {forecast_desc}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
                    count += 1
                    if count == 3:
                        break
        
            st.markdown("</div>", unsafe_allow_html=True)
        

        # ✅ Collect forecast data for temperature trend
        temps = []
        dates = []
        
        for entry in forecast_data["list"]:
            if "12:00:00" in entry["dt_txt"]:
                dates.append(entry["dt_txt"].split()[0])
                temps.append(entry["main"]["temp"])
        
        # ✅ Wind direction
        wind_deg = data["wind"]["deg"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        
        wind_dir = ""
        if 0 <= wind_deg < 90:
            wind_dir = "↗️ NE"
        elif 90 <= wind_deg < 180:
            wind_dir = "↘️ SE"
        elif 180 <= wind_deg < 270:
            wind_dir = "↙️ SW"
        else:
            wind_dir = "↖️ NW"
        
        # ✅ Build colD section
        with colD:
            st.markdown("""
                <div style='background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; box-shadow: 2px 2px 12px rgba(0,0,0,0.2); color: white;'>
                    <h4 style='text-align:center;'>📈 Temperature Trend (Next 3 Days)</h4>
            """, unsafe_allow_html=True)
        
            # 📊 Temperature chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=temps,
                mode='lines+markers',
                name='Temp (°C)',
                line=dict(color='orange', width=3),
                marker=dict(size=8)
            ))
            fig.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.05)',
        
            font=dict(
                color='black',
                family='Segoe UI',
                size=14
            ),
        
            xaxis=dict(
                title=dict(
                    text="Date",
                    font=dict(
                        size=16,
                        color='black',
                        family='Segoe UI Bold'
                    )
                ),
                tickfont=dict(
                    size=13,
                    color='black',
                    family='Segoe UI Bold'
                )
            ),
        
            yaxis=dict(
                title=dict(
                    text="Temp (°C)",
                    font=dict(
                        size=16,
                        color='black',
                        family='Segoe UI Bold'
                    )
                ),
                tickfont=dict(
                    size=13,
                    color='black',
                    family='Segoe UI Bold'
                )
            )
        )

            st.plotly_chart(fig, use_container_width=True)
        
            # 🌬️ Wind + Pressure box
            st.markdown(f"""
                <div style='margin-top: 20px; text-align: center; background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px;'>
                    <h5 style='margin-bottom: 10px;'>🧭 Wind & Pressure Overview</h5>
                    <p style='margin: 5px;'>💨 Wind Speed: <b>{wind_speed} m/s</b></p>
                    <p style='margin: 5px;'>🧭 Direction: <b>{wind_dir} ({wind_deg}°)</b></p>
                    <p style='margin: 5px;'>🔵 Pressure: <b>{pressure} hPa</b></p>
                </div>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.error("City not found. Please try again.")


