# 🌦️ Real-Time Weather Dashboard
A sleek, interactive real-time weather dashboard built using Streamlit and the OpenWeatherMap API. Users can enter a city name and view current weather details, sunrise/sunset times, and a 3-day forecast — all presented with weather-themed backgrounds and stylish UI components.

**🔍 Project Overview**
This project fetches and displays weather data in real time using the OpenWeatherMap API. It is designed with a responsive layout and includes background visuals that change based on the weather condition.

**✨ Key Features**
✅ Real-time weather updates for any city
✅ Weather-specific dynamic background images
✅ Display of:

Temperature, Humidity, Wind Speed, Pressure

Weather condition (Cloudy, Rainy, Sunny, etc.)

Sunrise and Sunset time
✅ 3-day forecast using the OpenWeatherMap Forecast API
✅ Stylish UI built with Streamlit and PIL (Python Imaging Library)
✅ Hosted and shareable via Streamlit Cloud

**🖥️ Tech Stack**
Python

Streamlit (Web UI)

OpenWeatherMap API

PIL (for background image processing)

Datetime & Requests

**Sample Video **



https://github.com/user-attachments/assets/95c4499b-1952-45b0-8330-e9de86ace593



**⚙️ How to Run Locally**
1.Clone the repository:

git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard


2.Install dependencies:

pip install -r requirements.txt

3.Get your OpenWeatherMap API key:

Go to https://openweathermap.org/

Create an account and generate your API key.

4.Add your API key in the script (or use .env for security):
API_KEY = "your_openweathermap_api_key"

5.Run the app:
streamlit run main.py
