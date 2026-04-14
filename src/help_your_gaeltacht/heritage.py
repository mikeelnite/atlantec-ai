"""Helpers for querying nearby heritage assets."""

import math

import requests

from help_your_gaeltacht.nearest_towns import haversine_distance

# National Heritage 250K Map of Ireland from Tailte Eireann
HERITAGE_FEATURESERVER = (
    "https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/"
    "Heritage___OSi_National_250K_Map_Of_Ireland/FeatureServer/0"
)


def _bounding_box(lat, lon, radius_km):
    """Build a rough WGS84 bounding box around a point."""
    lat_delta = radius_km / 111.0
    lon_scale = max(0.1, abs(math.cos(math.radians(lat))))
    lon_delta = radius_km / (111.0 * lon_scale)
    return (
        lon - lon_delta,
        lat - lat_delta,
        lon + lon_delta,
        lat + lat_delta,
    )


def query_heritage_assets(lat, lon, radius_km=5, limit=5, timeout=15):
    """Query ArcGIS Heritage Assets FeatureServer for features near a location."""
    search_radii = [radius_km]
    expanded_radius = max(radius_km * 4, 20)
    if expanded_radius not in search_radii:
        search_radii.append(expanded_radius)

    for active_radius_km in search_radii:
        min_lon, min_lat, max_lon, max_lat = _bounding_box(lat, lon, active_radius_km)
        params = {
            "f": "json",
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
            "outSR": "4326",
            "inSR": "4326",
            "geometry": f"{min_lon},{min_lat},{max_lon},{max_lat}",
            "geometryType": "esriGeometryEnvelope",
            "spatialRel": "esriSpatialRelIntersects",
            "resultRecordCount": 100,
        }

        try:
            response = requests.get(
                HERITAGE_FEATURESERVER + "/query",
                params=params,
                timeout=timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to query heritage assets: {exc}")

        if "error" in data:
            raise RuntimeError(f"Heritage Assets API error: {data['error']}")

        assets = []
        seen = set()
        for feature in data.get("features", []):
            props = feature.get("attributes", {})
            geometry = feature.get("geometry", {})
            if not geometry:
                continue

            asset_lat = geometry.get("y")
            asset_lon = geometry.get("x")
            if asset_lat is None or asset_lon is None:
                continue

            distance = haversine_distance(lat, lon, asset_lat, asset_lon)
            if distance > active_radius_km:
                continue

            name = (
                props.get("NAMN1")
                or props.get("Name")
                or props.get("AssetName")
                or props.get("SITE_NAME")
                or "Heritage Site"
            )
            asset_type = (
                props.get("CLASSDESC")
                or props.get("AssetType")
                or props.get("Type")
                or props.get("SITE_TYPE")
                or "Heritage Asset"
            )
            dedupe_key = (name, round(asset_lat, 5), round(asset_lon, 5))
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)

            assets.append(
                {
                    "name": name,
                    "type": asset_type,
                    "latitude": asset_lat,
                    "longitude": asset_lon,
                    "distance_km": round(distance, 1),
                    "properties": props,
                    "search_radius_km": active_radius_km,
                }
            )

        assets.sort(key=lambda x: x["distance_km"])
        if assets:
            return assets[:limit]

    return []
