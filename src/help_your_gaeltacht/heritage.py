import requests

from help_your_gaeltacht.nearest_towns import haversine_distance

# National Heritage 250K Map of Ireland from Tailte Éireann
HERITAGE_FEATURESERVER = "https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/Heritage___OSi_National_250K_Map_Of_Ireland/FeatureServer/0"


def query_heritage_assets(lat, lon, radius_km=5, limit=5, timeout=15):
    """Query ArcGIS Heritage Assets FeatureServer for features near a location."""
    distance_m = radius_km * 1000
    params = {
        "f": "json",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "resultRecordCount": 500,
    }
    
    try:
        response = requests.get(HERITAGE_FEATURESERVER + "/query", params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to query heritage assets: {exc}")
    
    if "error" in data:
        raise RuntimeError(f"Heritage Assets API error: {data['error']}")
    
    assets = []
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
        
        if distance * 1000 > distance_m:
            continue
        
        # Name field in national heritage dataset
        name = props.get("NAMN1") or props.get("Name") or props.get("AssetName") or "Heritage Site"
        asset_type = props.get("CLASSDESC") or props.get("AssetType") or props.get("Type") or "Heritage Asset"
        
        assets.append({
            "name": name,
            "type": asset_type,
            "latitude": asset_lat,
            "longitude": asset_lon,
            "distance_km": round(distance, 1),
            "properties": props,
        })
    
    assets.sort(key=lambda x: x["distance_km"])
    return assets[:limit]
