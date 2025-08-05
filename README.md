# <p align="center">SmartFlow-Prep</p>

SmartFlow-Prep is the data preprocessing pipeline for the SmartFlow system. It collects, cleans, and enriches historical
CitiBike trip data with contextual features such as weather, time, holidays, and station metadata. The processed output
serves as the structured input for SmartFlow’s bike rebalancing model.

## Data Processing Pipeline

The pipeline consists of several scripts that perform sequential data fetching, enrichment, and cleaning tasks.

### 1. Fetching Initial Data

* **Station Metadata:** The first step fetches station information from the CitiBike GBFS feed. The script
  `scripts/fetch_station_metadata.py` retrieves data on all stations and saves it to `data/metadata/stations_info.csv`.

* **Weather Data:** The `scripts/fetch_weather.py` script obtains historical weather data for New York City for the
  years 2015, 2016, and 2017. It uses the Visual Crossing Weather API and saves the output to
  `data/weather/nyc_weather_2015_2017.csv`.

### 2. Data Enrichment

* **Temporal Features:** The `scripts/enrich_temporal.py` script processes the raw trip data from
  `data/citibike/New York CitiBike - 2015-2017.csv`. It extracts temporal features such as the date, hour, weekday, and
  whether the day is a weekend, saving the enriched data to `data/enriched/trips_with_temporal.csv`.

* **Station Elevation:** To add topographical data, the `scripts/enrich_station_elevation.py` script fetches the
  elevation for each station using the Open-Elevation API. This script takes the station information, retrieves
  elevation data, and saves the result to `data/metadata/stations_with_elevation.csv`.

### 3. Data Cleaning

* **Trip Data Cleaning:** The `scripts/clean_temporal_data.py` script cleans the enriched trip data. It handles missing
  coordinates, converts trip durations to a numerical format, removes trips with non-positive durations, and adds a flag
  for U.S. holidays. The cleaned data is saved to `data/enriched/trips_cleaned.csv`.

### 4. Merging and Finalizing Data

* **Merging Weather Data:** The `scripts/merge_weather_into_trips.py` script merges the cleaned trip data with the
  historical weather data. The two datasets are joined on the date, and the final combined dataset is saved as
  `data/enriched/trips_final.csv`.

* **Finalizing Station Metadata:** The `scripts/prepare_station_metadata.py` script standardizes the station names from
  the trip data and the station metadata. It then filters the metadata to include only the stations present in the trip
  data and saves the final, cleaned station metadata to `data/enriched/stations_final.csv`.

## Repository Structure

* **`/data`**: This directory contains the raw, enriched, and final datasets.
    * `/data/citibike`: Raw trip data.
    * `/data/enriched`: Intermediate and final processed datasets.
    * `/data/metadata`: Station metadata files.
    * `/data/weather`: Raw weather data.
* **`/scripts`**: This directory contains all the Python scripts used for the data processing pipeline.
* **`.gitignore`**: Specifies files and directories to be ignored by Git.
* **`.gitattributes`**: Specifies attributes for paths, in this case, to handle large CSV files with Git LFS.
* **`LICENSE`**: The project is licensed under the MIT License.
* **`.idea`**: Project-specific settings for the JetBrains IDE.