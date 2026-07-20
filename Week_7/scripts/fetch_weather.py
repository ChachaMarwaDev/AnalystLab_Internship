"""
fetch_weather.py

Pulls real-time weather data from the OpenWeather Current Weather API
for a list of cities and stores the results in a pandas DataFrame / CSV.

Setup:
    pip install requests pandas python-dotenv
    Create a .env file in the same folder as this script containing:
        OPENWEATHER_API_KEY=your_key_here
    (Add .env to your .gitignore so the key never gets committed to GitHub.)
"""

import os
import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()  # reads .env in the current directory and loads it into os.environ

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITIES = ["Nairobi", "Migori", "London", "New York", "Tokyo"]

UNITS = "metric"  # metric = Celsius & m/s; use "imperial" for Fahrenheit & mph


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def get_weather(city: str) -> dict | None:
    """Fetch current weather for a single city. Returns None on failure."""
    params = {"q": city, "appid": API_KEY, "units": UNITS}

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[WARN] Could not fetch '{city}': {response.status_code} - {response.json().get('message', '')}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[WARN] Network error fetching '{city}': {e}")
        return None

    data = response.json()

    return {
        "City Name": data.get("name", city),
        "Temperature (C)": data["main"]["temp"],
        "Humidity (%)": data["main"]["humidity"],
        "Weather Condition": data["weather"][0]["description"].title(),
        "Wind Speed (m/s)": data["wind"]["speed"],
        "Date & Time (UTC)": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }


def fetch_all(cities: list[str]) -> pd.DataFrame:
    """Fetch weather for a list of cities and return as a DataFrame."""
    records = []
    for city in cities:
        result = get_weather(city)
        if result:
            records.append(result)
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY_HERE":
        raise SystemExit(
            "No API key found. Set OPENWEATHER_API_KEY as an environment "
            "variable, or replace API_KEY in the script."
        )

    weather_df = fetch_all(CITIES)

    if weather_df.empty:
        print("No weather data retrieved. Check your API key and city names.")
    else:
        print(weather_df.to_string(index=False))
        weather_df.to_csv("weather_data.csv", index=False)
        print("\nSaved to weather_data.csv")