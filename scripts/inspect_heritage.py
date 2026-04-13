import requests
import json

resp = requests.get(
    "https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/Heritage___OSi_National_250K_Map_Of_Ireland/FeatureServer/0/query",
    params={"f": "json", "where": "1=1", "outFields": "*", "resultRecordCount": 1},
    timeout=10,
)
data = resp.json()
if data.get("features"):
    feat = data["features"][0]
    attrs = feat.get("attributes", {})
    print("Field names available:")
    for key in sorted(attrs.keys()):
        print(f"  {key}: {attrs[key]}")
    print("\nGeometry:")
    print(f"  Type: {feat.get('geometry', {}).get('type', 'unknown')}")
    print(f"  Keys: {list(feat.get('geometry', {}).keys())}")
