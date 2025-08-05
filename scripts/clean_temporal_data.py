from pathlib import Path

import holidays
import pandas as pd

# Project root and paths
ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "enriched" / "trips_with_temporal.csv"
OUTPUT_FILE = ROOT / "data" / "enriched" / "trips_cleaned.csv"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

print(f"📥 Loading input: {INPUT_FILE}")
df = pd.read_csv(INPUT_FILE, parse_dates=["Start Time", "Stop Time"], low_memory=False)
print(f"✅ Loaded {len(df):,} rows")

# ─────────────────────────────────────────────
# Drop invalid coordinates
before = len(df)
df = df.dropna(subset=[
    "Start Station Latitude", "Start Station Longitude",
    "End Station Latitude", "End Station Longitude"
])
print(f"🧭 Dropped {before - len(df):,} rows with missing coordinates")

# Convert durations
df["Trip Duration"] = pd.to_numeric(df["Trip Duration"], errors="coerce")
df["Trip_Duration_in_min"] = pd.to_numeric(df["Trip_Duration_in_min"], errors="coerce")

# Drop incomplete entries
before = len(df)
df = df.dropna(subset=[
    "Trip Duration", "Trip_Duration_in_min",
    "Start Station Name", "End Station Name"
])
print(f"🧹 Dropped {before - len(df):,} rows with missing duration or station names")

# Remove non-positive durations
before = len(df)
df = df[df["Trip Duration"] > 0]
print(f"⏱️ Removed {before - len(df):,} rows with zero or negative duration")

# ─────────────────────────────────────────────
# Add US holiday flag (optional)
df["date"] = pd.to_datetime(df["date"]).dt.date
us_holidays = holidays.US(years=[2015, 2016, 2017])
df["is_holiday"] = df["date"].isin(us_holidays)
print("📅 Added is_holiday flag using US federal holidays")

# ─────────────────────────────────────────────
# Save final output
df.to_csv(OUTPUT_FILE, index=False)
print(f"💾 Saved cleaned file to: {OUTPUT_FILE}")
print(f"✅ Final row count: {len(df):,}")
