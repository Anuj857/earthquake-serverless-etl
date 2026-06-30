import json
import os
import requests

# Dataset Name : (API URL, Output File)
DATASETS = {
    "earthquake": (
        "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
        "sample_earthquake.json"
    ),
    "weather": (
        "https://api.open-meteo.com/v1/forecast?latitude=28.6139&longitude=77.2090&current=temperature_2m,relative_humidity_2m,wind_speed_10m",
        "sample_weather.json"
    ),
    "air_quality": (
        "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=28.6139&longitude=77.2090&current=pm10,pm2_5",
        "sample_air_quality.json"
    ),
    "products": (
        "https://fakestoreapi.com/products",
        "sample_products.json"
    ),
    "government": (
        "https://data.cityofnewyork.us/resource/erm2-nwe9.json?$limit=50",
        "sample_government.json"
    )
}

# Create sample_data folder
os.makedirs("sample_data", exist_ok=True)

# Fetch all datasets
for dataset, (url, filename) in DATASETS.items():

    print(f"\nFetching {dataset} data...")

    try:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:

            with open(
                os.path.join("sample_data", filename),
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(response.json(), file, indent=4)

            print(f"✅ {filename} saved successfully!")

        else:
            print(f"❌ Failed to fetch {dataset}. Status Code: {response.status_code}")

    except Exception as e:
        print(f"❌ Error fetching {dataset}: {e}")

print("\n🎉 All datasets processed.")