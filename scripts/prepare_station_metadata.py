from pathlib import Path

import pandas as pd

# Paths
ROOT = Path(__file__).resolve().parents[1]
TRIP_FILE = ROOT / "data" / "enriched" / "trips_cleaned.csv"
STATION_FILE = ROOT / "data" / "metadata" / "stations_with_elevation.csv"
OUT_FILE = ROOT / "data" / "enriched" / "stations_final.csv"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load
print("📥 Loading trip data and station metadata...")
trips = pd.read_csv(TRIP_FILE)
stations = pd.read_csv(STATION_FILE)


# Standardize names (lowercase, no spaces)
def normalize(name): return str(name).strip().lower()


stations["name_norm"] = stations["name"].apply(normalize)
start_names = trips["Start Station Name"].dropna().unique()
end_names = trips["End Station Name"].dropna().unique()
all_names = pd.Series(list(set(start_names) | set(end_names)))
all_names = all_names.dropna().drop_duplicates().apply(normalize)

# Filter station metadata
stations = stations[stations["name_norm"].isin(all_names)]
stations = stations.drop_duplicates(subset=["station_id"])
stations = stations.rename(columns={
    "name": "Station Name",
    "lat": "Latitude",
    "lon": "Longitude"
})[["station_id", "Station Name", "Latitude", "Longitude", "capacity", "elevation_m"]]

stations.to_csv(OUT_FILE, index=False)
print(f"✅ Final station metadata saved to: {OUT_FILE}")
