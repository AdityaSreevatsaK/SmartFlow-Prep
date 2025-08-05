import os
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")

if not API_KEY:
    raise ValueError("❌ VISUAL_CROSSING_API_KEY not found in .env file.")

# Get project root and define output path
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "data" / "weather" / "nyc_weather_2015_2017.csv"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

print(f"🌍 Fetching weather data for: New York, NY")
print(f"📤 Target file: {OUTPUT_FILE}")

# Fetch weather per year
YEARS = ["2015", "2016", "2017"]
UNIT = "metric"
dfs = []

for year in YEARS:
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"New York, NY/{start_date}/{end_date}"
        f"?unitGroup={UNIT}&include=days&key={API_KEY}&contentType=csv"
    )

    print(f"\n📡 Fetching weather for {year}...")
    try:
        response = requests.get(url)

        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            dfs.append(df)
            print(f"✅ Success: {len(df):,} rows fetched for {year}")
        else:
            print(f"❌ Failed to fetch {year}: HTTP {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"💥 Error fetching {year}: {e}")

# Combine and save
if dfs:
    all_weather = pd.concat(dfs, ignore_index=True)
    all_weather.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Weather data saved to: {OUTPUT_FILE}")
    print(f"📊 Total rows fetched: {len(all_weather):,}")
else:
    print("\n❌ No data fetched. Nothing to save.")
