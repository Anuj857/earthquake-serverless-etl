import json
import requests
import os

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

response = requests.get(URL)

if response.status_code == 200:

    os.makedirs("sample_data", exist_ok=True)

    with open("sample_data/sample_earthquake.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4)

    print("Sample data saved successfully!")

else:
    print("Failed to fetch data.")