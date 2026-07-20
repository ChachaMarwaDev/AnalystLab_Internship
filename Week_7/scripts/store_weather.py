"""
store_weather.py

STEP 3 — STORE.
Takes the cleaned weather data produced by clean_weather.py and persists
it into a local SQLite database, appending each run as a new snapshot so
you build up a history of readings over time (rather than overwriting).

Duplicate handling: a UNIQUE constraint on (city_name, retrieved_at_utc)
means the same city + timestamp can only be stored once. Re-running the
script with the same cleaned CSV will not create duplicate rows.

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

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CLEAN_INPUT_FILE = DATA_DIR / "weather_data_clean.csv"
DB_FILE = DATA_DIR / "weather_data.db"
TABLE_NAME = "weather_readings"

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    city_name TEXT NOT NULL,
    temperature_c REAL NOT NULL,
    humidity_pct INTEGER NOT NULL,
    weather_condition TEXT NOT NULL,
    wind_speed_mps REAL NOT NULL,
    retrieved_at_utc TEXT NOT NULL,
    UNIQUE(city_name, retrieved_at_utc)
);
"""


# ---------------------------------------------------------------------------
# Store — append cleaned data into SQLite, skipping duplicates
# ---------------------------------------------------------------------------
def store_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str) -> tuple[int, int]:
    """
    Insert the cleaned DataFrame into a SQLite table, creating the table on
    first run. Rows that violate the UNIQUE(city_name, retrieved_at_utc)
    constraint (i.e. already stored) are silently skipped via INSERT OR IGNORE.

    Returns (rows_inserted, rows_skipped_as_duplicates).
    """
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(CREATE_TABLE_SQL)

        before_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

        rows = df.to_dict("records")
        conn.executemany(
            f"""
            INSERT OR IGNORE INTO {table_name}
                (city_name, temperature_c, humidity_pct, weather_condition, wind_speed_mps, retrieved_at_utc)
            VALUES (:city_name, :temperature_c, :humidity_pct, :weather_condition, :wind_speed_mps, :retrieved_at_utc)
            """,
            rows,
        )
        conn.commit()

        after_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    finally:
        conn.close()

    rows_inserted = after_count - before_count
    rows_skipped = len(df) - rows_inserted
    return rows_inserted, rows_skipped


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not Path(CLEAN_INPUT_FILE).exists():
        raise SystemExit(
            f"'{CLEAN_INPUT_FILE}' not found. Run fetch_weather.py then "
            f"clean_weather.py first to generate it."
        )

    clean_df = pd.read_csv(CLEAN_INPUT_FILE)
    # Store the timestamp as ISO text so the UNIQUE constraint compares cleanly.
    clean_df["retrieved_at_utc"] = pd.to_datetime(clean_df["retrieved_at_utc"]).astype("string")

    if clean_df.empty:
        print("No data to store — cleaned file was empty.")
    else:
        inserted, skipped = store_to_sqlite(clean_df, DB_FILE, TABLE_NAME)

        print(f"Inserted {inserted} new row(s) into '{TABLE_NAME}' table in {DB_FILE}")
        if skipped:
            print(f"Skipped {skipped} duplicate row(s) (already stored for that city + timestamp)")

        conn = sqlite3.connect(DB_FILE)
        total_rows = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
        preview = pd.read_sql(
            f"SELECT * FROM {TABLE_NAME} ORDER BY retrieved_at_utc DESC LIMIT 5",
            conn,
        )
        conn.close()

        print(f"Total rows in table now: {total_rows}\n")
        print("Most recent rows in the database:")
        print(preview.to_string(index=False))