"""
store_weather.py

STEP 3 — STORE.
Takes the cleaned weather data produced by clean_weather.py and persists
it into a local SQLite database, appending each run as a new snapshot so
you build up a history of readings over time (rather than overwriting).

Why SQLite over CSV/Excel here: this pipeline is meant to run repeatedly
(e.g. once a day), and a database handles repeated appends, querying, and
growing data volume far better than re-writing a flat file each time.

Setup:
    pip install pandas
Run fetch_weather.py then clean_weather.py first to generate the input CSV.
"""

import sqlite3
import pandas as pd
from pathlib import Path

CLEAN_INPUT_FILE = "weather_data_clean.csv"
DB_FILE = "weather_data.db"
TABLE_NAME = "weather_readings"


# ---------------------------------------------------------------------------
# Store — append cleaned data into SQLite
# ---------------------------------------------------------------------------
def store_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str) -> int:
    """
    Append the cleaned DataFrame to a SQLite table, creating the table and
    database file on first run. Returns the number of rows written.
    """
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    finally:
        conn.close()

    return row_count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not Path(CLEAN_INPUT_FILE).exists():
        raise SystemExit(
            f"'{CLEAN_INPUT_FILE}' not found. Run fetch_weather.py then "
            f"clean_weather.py first to generate it."
        )

    clean_df = pd.read_csv(CLEAN_INPUT_FILE, parse_dates=["retrieved_at_utc"])

    if clean_df.empty:
        print("No data to store — cleaned file was empty.")
    else:
        total_rows = store_to_sqlite(clean_df, DB_FILE, TABLE_NAME)

        print(f"Stored {len(clean_df)} new row(s) into '{TABLE_NAME}' table in {DB_FILE}")
        print(f"Total rows in table now: {total_rows}")

        # Quick sanity check: show the most recent readings back from the DB.
        conn = sqlite3.connect(DB_FILE)
        preview = pd.read_sql(
            f"SELECT * FROM {TABLE_NAME} ORDER BY retrieved_at_utc DESC LIMIT 5",
            conn,
        )
        conn.close()
        print("\nMost recent rows in the database:")
        print(preview.to_string(index=False))