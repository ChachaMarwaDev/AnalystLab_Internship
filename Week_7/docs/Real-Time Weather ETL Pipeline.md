# Real-Time Weather ETL Pipeline

A lightweight ETL (Extract, Transform, Load) pipeline that pulls live weather
data for multiple cities from the OpenWeather API, cleans and standardizes
it, and stores it in a local SQLite database for historical tracking.

Built as part of my data engineering portfolio (AnalystLab Africa Internship,
Week 7).

---

## Project Overview

This project demonstrates a small but complete ETL workflow: connecting to a
third-party REST API, structuring the raw JSON response into a tabular
format, cleaning and standardizing it for analysis, and persisting it to a
database with duplicate protection — the same pattern used in production
data pipelines, just at a smaller scale.

The pipeline can be run as a one-off snapshot or repeatedly (e.g. on a daily
schedule) to build up a time-series history of weather readings per city.

## Data Source

- **API:** [OpenWeather Current Weather Data API](https://openweathermap.org/current)
- **Endpoint:** `https://api.openweathermap.org/data/2.5/weather`
- **Access:** Free tier, authenticated via a personal API key
- **Cities tracked:** Nairobi, Migori, London, New York, Tokyo
- **Fields captured:** City Name, Temperature (°C), Humidity (%), Weather
  Condition, Wind Speed (m/s), Date & Time of retrieval (UTC)

## ETL Steps

### 1. Extract — `fetch_weather.py`
- Connects to the OpenWeather API using the `requests` library
- Sends one request per city with the API key (loaded securely from a
  `.env` file, never hardcoded)
- Handles request failures gracefully (invalid city, bad API key, network
  errors) without crashing the run
- Saves the raw pull to `data/weather_data.csv`

### 2. Transform — `clean_weather.py`
- Renames raw fields into clear, consistent `snake_case` column names
  (e.g. `Temperature (C)` → `temperature_c`)
- Casts each column to an explicit, correct data type (floats for
  temperature/wind speed, integer for humidity, string for text fields,
  proper `datetime` for the timestamp)
- Standardizes text formatting (e.g. weather conditions to title case)
- Saves the cleaned table to `data/weather_data_clean.csv`

### 3. Load — `store_weather.py`
- Persists the cleaned data into a local SQLite database
  (`data/weather_data.db`)
- Enforces a `UNIQUE(city_name, retrieved_at_utc)` constraint so re-running
  the pipeline never creates duplicate records
- Reports how many new rows were inserted vs. skipped as duplicates on
  each run

### Orchestration — `main.py`
- Runs all three steps end-to-end with a single command, passing data
  between stages in memory while still saving each stage's output file

## Tools Used

| Tool | Purpose |
|---|---|
| Python 3.13 | Core language |
| `requests` | API calls to OpenWeather |
| `pandas` | Data structuring, cleaning, type casting |
| `sqlite3` (standard library) | Local database storage |
| `python-dotenv` | Secure API key management via `.env` |
| Git / GitHub | Version control |

## Project Structure

```
Week_7/
├── docs/
├── data/                     # generated output — gitignored
│   ├── weather_data.csv
│   ├── weather_data_clean.csv
│   └── weather_data.db
└── scripts/
    ├── main.py                # run this to execute the full pipeline
    ├── fetch_weather.py        # Step 1: Extract
    ├── clean_weather.py        # Step 2: Transform
    └── store_weather.py        # Step 3: Load
```

## How to Run

```bash
# from inside the scripts/ folder
pip install requests pandas python-dotenv

# create a .env file in scripts/ containing:
# OPENWEATHER_API_KEY=your_key_here

python main.py
```

## Top Findings

From an initial snapshot pull across the five tracked cities:

- **Wide temperature spread across cities at the same moment in time:**
  readings ranged from 12.5°C (London) to 35.1°C (Tokyo) in a single pull,
  underscoring how much location affects "current weather" — a reminder
  that any downstream analysis needs to be city-aware rather than
  aggregated blindly.
- **Humidity and conditions track together:** the highest humidity reading
  (Nairobi, 87%) coincided with clear skies, while overcast cities (London,
  Migori) sat in the 63–74% range — a useful sanity check that the data
  behaves as physically expected.
- **Wind speed was the least variable metric** across cities (0.45–2.68
  m/s), suggesting temperature and conditions are more useful signals than
  wind speed for day-to-day city comparisons at this scale.
- **Data quality:** after cleaning, all fields cast cleanly to their target
  types with no null values — confirming the API's raw JSON is reliably
  structured and the transform step's column mapping is correct.

*(Note: these findings reflect a single point-in-time pull. Running the
pipeline daily and querying `weather_data.db` over time would allow for
genuine trend analysis — e.g. seasonal patterns or volatility per city —
rather than a one-off comparison.)*

## Future Improvements

- Schedule `main.py` to run automatically (e.g. via cron or Task
  Scheduler) to build a real historical dataset
- Add a visualization layer (matplotlib/seaborn) to chart temperature and
  humidity trends per city over time
- Extend to a forecast endpoint for predictive comparisons against actual
  outcomes

---
*Generated from `main.py` — AnalystLab Internship portfolio project.*