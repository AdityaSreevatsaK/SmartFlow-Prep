import time
from pathlib import Path

import pandas as pd
import requests

# Paths
ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / "data" / "metadata" / "stations_info.csv"
OUT_FILE = ROOT / "data" / "metadata" / "stations_with_elevation.csv"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load station data
if not IN_FILE.exists():
    raise FileNotFoundError(f"❌ Station info file not found: {IN_FILE}")
df = pd.read_csv(IN_FILE)
print(f"📥 Loaded {len(df)} stations")

# Prepare coordinate strings
coordinates = df[["lat", "lon"]].apply(lambda row: f"{row.lat},{row.lon}", axis=1).tolist()

# Batch requests (Open-Elevation allows ~100 per batch)
batch_size = 90
elevation_results = []

print("⛰️ Fetching elevation data from Open-Elevation...")
for i in range(0, len(coordinates), batch_size):
    chunk = coordinates[i:i + batch_size]
    loc_param = "|".join(chunk)
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={loc_param}"

    try:
        r = requests.get(url)
        r.raise_for_status()
        elevation_results.extend(r.json()["results"])
        time.sleep(1)  # Be nice to the API :)
    except Exception as e:
        print(f"❌ Batch {i // batch_size + 1} failed: {e}")

# Combine and save
if elevation_results:
    elev_df = pd.DataFrame(elevation_results)
    df = df.reset_index(drop=True)
    df["elevation_m"] = elev_df["elevation"]
    df.to_csv(OUT_FILE, index=False)
    print(f"\n✅ Saved station metadata with elevation to: {OUT_FILE}")
else:
    print("❌ No elevation data retrieved.")
