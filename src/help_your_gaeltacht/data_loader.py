import json
from pathlib import Path

import requests


def load_local_geojson(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data.get("features", [])


def fetch_arcgis_features(endpoint_url, params=None):
    params = params or {
        "f": "geojson",
        "where": "1=1",
        "outFields": "*",
    }
    response = requests.get(endpoint_url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data.get("features", [])


def load_custom_town_list(path="datasets/gael_towns.geojson"):
    return load_local_geojson(path)
