"""
clean_weather.py

STEP 2 — NORMALIZE & CLEAN.
Reads the raw JSON saved by fetch_weather.py, flattens it into a pandas
DataFrame, and cleans it into an analysis-ready table:
    - renames columns for clarity
    - casts each column to an explicit, correct dtype
    - standardizes text formatting and timestamps

Setup:
    pip install pandas
Run fetch_weather.py first to generate raw_weather_data.json.
"""

import json
import pandas as pd
from datetime import datetime, timezone

RAW_INPUT_FILE = "raw_weather_data.json"
CLEAN_OUTPUT_FILE = "weather_data_clean.csv"


# ---------------------------------------------------------------------------
# Normalize — flatten nested JSON into a flat DataFrame
# ---------------------------------------------------------------------------
def normalize_responses(raw_responses: list[dict]) -> pd.DataFrame:
    """
    Flatten the nested JSON (main.temp, weather[0].description, wind.speed,
    etc. are all nested) into a single flat table using json_normalize.
    """
    if not raw_responses:
        return pd.DataFrame()

    df = pd.json_normalize(raw_responses, sep="_")

    # 'weather' is itself a list of dicts (usually length 1) so json_normalize
    # can't flatten it directly — pull out the description manually.
    df["weather_description"] = df["weather"].apply(
        lambda w: w[0]["description"] if isinstance(w, list) and w else None
    )

    return df


# ---------------------------------------------------------------------------
# Clean — rename, cast types, standardize units/format
# ---------------------------------------------------------------------------
def clean_weather_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Take the flattened raw DataFrame and produce an analysis-ready table:
    - select and rename only the relevant columns
    - cast each column to an explicit, correct dtype
    - standardize text formatting and timestamps
    """
    if raw_df.empty:
        return pd.DataFrame()

    df = raw_df.copy()

    # Select just the columns we need, renamed for clarity.
    column_map = {
        "name": "city_name",
        "main_temp": "temperature_c",
        "main_humidity": "humidity_pct",
        "weather_description": "weather_condition",
        "wind_speed": "wind_speed_mps",
        "dt": "observation_unix",
    }
    df = df[list(column_map.keys())].rename(columns=column_map)

    # --- Type casting ---
    df["city_name"] = df["city_name"].astype("string")
    df["temperature_c"] = pd.to_numeric(df["temperature_c"], errors="coerce").astype("float64")
    df["humidity_pct"] = pd.to_numeric(df["humidity_pct"], errors="coerce").astype("int64")
    df["wind_speed_mps"] = pd.to_numeric(df["wind_speed_mps"], errors="coerce").astype("float64")

    # --- Standardization ---
    # Title-case weather descriptions ("clear sky" -> "Clear Sky") for consistent display.
    df["weather_condition"] = df["weather_condition"].astype("string").str.title()

    # OpenWeather's 'dt' field is Unix UTC time for the observation itself —
    # convert it to a proper timestamp rather than using the local request time.
    df["observation_time_utc"] = pd.to_datetime(df["observation_unix"], unit="s", utc=True)
    df = df.drop(columns=["observation_unix"])

    # Snapshot time: when this cleaning step actually ran.
    df["retrieved_at_utc"] = datetime.now(timezone.utc)

    # Reorder into a clean, final column order.
    df = df[
        [
            "city_name",
            "temperature_c",
            "humidity_pct",
            "weather_condition",
            "wind_speed_mps",
            "observation_time_utc",
            "retrieved_at_utc",
        ]
    ]

    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        with open(RAW_INPUT_FILE, "r") as f:
            raw = json.load(f)
    except FileNotFoundError:
        raise SystemExit(
            f"'{RAW_INPUT_FILE}' not found. Run fetch_weather.py first to generate it."
        )

    normalized_df = normalize_responses(raw)
    clean_df = clean_weather_data(normalized_df)

    if clean_df.empty:
        print("No data to clean — raw file was empty.")
    else:
        print(clean_df.dtypes, "\n")
        print(clean_df.to_string(index=False))

        clean_df.to_csv(CLEAN_OUTPUT_FILE, index=False)
        print(f"\nSaved cleaned data to {CLEAN_OUTPUT_FILE}")