"""
main.py

Orchestrates the full weather pipeline in one run:
    1. fetch_weather  -> pulls raw data from the API, saves weather_data.csv
    2. clean_weather  -> normalizes/cleans it, saves weather_data_clean.csv
    3. store_weather   -> persists the cleaned data into weather_data.db

Usage:
    python main.py

Place this file in the same 'scripts' folder as fetch_weather.py,
clean_weather.py, and store_weather.py.
"""

import sys

import fetch_weather
import clean_weather
import store_weather


def run_pipeline() -> None:
    # --- Step 1: Fetch ---
    print("=" * 60)
    print("STEP 1/3: Fetching weather data...")
    print("=" * 60)

    if fetch_weather.API_KEY == "YOUR_API_KEY_HERE":
        print("[ERROR] No API key found. Set OPENWEATHER_API_KEY in your .env file.")
        sys.exit(1)

    weather_df = fetch_weather.fetch_all(fetch_weather.CITIES)

    if weather_df.empty:
        print("[ERROR] No weather data retrieved. Check your API key and city names.")
        sys.exit(1)

    weather_df.to_csv(fetch_weather.RAW_OUTPUT_FILE, index=False)
    print(f"Saved to {fetch_weather.RAW_OUTPUT_FILE}\n")

    # --- Step 2: Clean ---
    print("=" * 60)
    print("STEP 2/3: Cleaning and normalizing data...")
    print("=" * 60)

    clean_df = clean_weather.clean_weather_data(weather_df)

    if clean_df.empty:
        print("[ERROR] Cleaning produced no data.")
        sys.exit(1)

    clean_df.to_csv(clean_weather.CLEAN_OUTPUT_FILE, index=False)
    print(clean_df.to_string(index=False))
    print(f"\nSaved to {clean_weather.CLEAN_OUTPUT_FILE}\n")

    # --- Step 3: Store ---
    print("=" * 60)
    print("STEP 3/3: Storing data in SQLite...")
    print("=" * 60)

    # store_weather expects the timestamp as ISO text for the UNIQUE constraint.
    store_ready_df = clean_df.copy()
    store_ready_df["retrieved_at_utc"] = store_ready_df["retrieved_at_utc"].astype("string")

    inserted, skipped = store_weather.store_to_sqlite(
        store_ready_df, store_weather.DB_FILE, store_weather.TABLE_NAME
    )

    print(f"Inserted {inserted} new row(s) into '{store_weather.TABLE_NAME}' table in {store_weather.DB_FILE}")
    if skipped:
        print(f"Skipped {skipped} duplicate row(s) (already stored for that city + timestamp)")

    print("\nPipeline complete.")


if __name__ == "__main__":
    run_pipeline()