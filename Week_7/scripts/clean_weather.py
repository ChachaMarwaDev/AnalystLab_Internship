"""
clean_weather.py

STEP 2 — CLEAN.
Reads the raw, flat CSV produced by fetch_weather.py and cleans it into
an analysis-ready table:
    - renames columns for clarity (consistent snake_case)
    - casts each column to an explicit, correct dtype
    - standardizes text formatting and timestamps

Setup:
    pip install pandas
Run fetch_weather.py first to generate the raw CSV.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

RAW_INPUT_FILE = DATA_DIR / "weather_data.csv"
CLEAN_OUTPUT_FILE = DATA_DIR / "weather_data_clean.csv"


# ---------------------------------------------------------------------------
# Clean — rename, cast types, standardize units/format
# ---------------------------------------------------------------------------
def clean_weather_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Take the raw flat CSV DataFrame and produce an analysis-ready table:
    - select and rename only the relevant columns
    - cast each column to an explicit, correct dtype
    - standardize text formatting and timestamps
    """
    if raw_df.empty:
        return pd.DataFrame()

    df = raw_df.copy()

    # Select just the columns we need, renamed to clear, consistent snake_case.
    column_map = {
        "City Name": "city_name",
        "Temperature (C)": "temperature_c",
        "Humidity (%)": "humidity_pct",
        "Weather Condition": "weather_condition",
        "Wind Speed (m/s)": "wind_speed_mps",
        "Date & Time (UTC)": "retrieved_at_utc",
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

    # Parse the timestamp column into a real datetime dtype (was a plain string).
    df["retrieved_at_utc"] = pd.to_datetime(df["retrieved_at_utc"], utc=True)

    # Final column order.
    df = df[
        [
            "city_name",
            "temperature_c",
            "humidity_pct",
            "weather_condition",
            "wind_speed_mps",
            "retrieved_at_utc",
        ]
    ]

    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        raw_df = pd.read_csv(RAW_INPUT_FILE)
    except FileNotFoundError:
        raise SystemExit(
            f"'{RAW_INPUT_FILE}' not found. Run fetch_weather.py first to generate it."
        )

    clean_df = clean_weather_data(raw_df)

    if clean_df.empty:
        print("No data to clean — raw file was empty.")
    else:
        print(clean_df.dtypes, "\n")
        print(clean_df.to_string(index=False))

        clean_df.to_csv(CLEAN_OUTPUT_FILE, index=False)
        print(f"\nSaved cleaned data to {CLEAN_OUTPUT_FILE}")