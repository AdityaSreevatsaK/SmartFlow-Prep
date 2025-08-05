from pathlib import Path

import pandas as pd

# Paths
ROOT = Path(__file__).resolve().parents[1]
TRIP_FILE = ROOT / "data" / "enriched" / "trips_cleaned.csv"
WEATHER_FILE = ROOT / "data" / "weather" / "nyc_weather_2015_2017.csv"
OUT_FILE = ROOT / "data" / "enriched" / "trips_final.csv"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load data
print("📥 Loading trip and weather data...")
trips = pd.read_csv(TRIP_FILE, parse_dates=["Start Time"])
weather = pd.read_csv(WEATHER_FILE, parse_dates=["datetime"])

# Prepare weather data
weather["date"] = weather["datetime"].dt.date
weather = weather[["date", "temp", "precip", "windspeed", "conditions"]]

# Merge on date
print("🔗 Merging on 'date'...")
trips["date"] = pd.to_datetime(trips["date"]).dt.date
merged = pd.merge(trips, weather, on="date", how="left")

# Save
merged.to_csv(OUT_FILE, index=False)
print(f"✅ Merged trips + weather saved to: {OUT_FILE}")
