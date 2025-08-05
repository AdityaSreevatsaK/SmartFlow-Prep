from pathlib import Path

import pandas as pd
import requests

# Paths
ROOT = Path(__file__).resolve().parents[1]
OUT_FILE = ROOT / "data" / "metadata" / "stations_info.csv"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# URL to CitiBike GBFS station metadata
URL = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"

print("📡 Fetching station metadata from CitiBike GBFS...")

try:
    response = requests.get(URL)
    response.raise_for_status()
    stations = response.json()["data"]["stations"]
    df = pd.DataFrame(stations)
    df.to_csv(OUT_FILE, index=False)
    print(f"✅ Saved {len(df)} station entries to: {OUT_FILE}")
except Exception as e:
    print(f"❌ Failed to fetch station metadata: {e}")
