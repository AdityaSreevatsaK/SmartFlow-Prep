from pathlib import Path

import pandas as pd

# Get the project root (1 level up from /scripts)
ROOT = Path(__file__).resolve().parents[1]

# File paths
INPUT_FILE = ROOT / "data" / "citibike" / "New York CitiBike - 2015-2017.csv"
OUTPUT_FILE = ROOT / "data" / "enriched" / "trips_with_temporal.csv"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

print(f"📂 Looking for: {INPUT_FILE}")
print(f"📤 Will save to: {OUTPUT_FILE}")

# Check file exists
if not INPUT_FILE.exists():
    raise FileNotFoundError(f"❌ File not found: {INPUT_FILE}")

# Load
print("📥 Reading trip data...")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"✅ Loaded {len(df):,} rows")

# Parse Start Time
print("⏳ Converting 'Start Time' to datetime...")
df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce")
before = len(df)
df = df.dropna(subset=["Start Time"])
print(f"🧼 Dropped {before - len(df):,} rows with invalid Start Time")

# Extract temporal features
print("📅 Extracting temporal features...")
df["date"] = df["Start Time"].dt.date
df["hour"] = df["Start Time"].dt.hour
df["weekday"] = df["Start Time"].dt.weekday
df["is_weekend"] = df["weekday"].isin([5, 6])

# Save enriched file
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Enriched file saved at: {OUTPUT_FILE}")
print(f"📊 Final row count: {len(df):,}")
