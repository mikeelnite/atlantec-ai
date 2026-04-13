import requests

from help_your_gaeltacht.nearest_towns import haversine_distance

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
    "https://overpass.osm-planet.ch/api/interpreter",
]


def parse_overpass_element(element):
    tags = element.get("tags", {})
    name = tags.get("name") or tags.get("operator") or "Unnamed Pub"
    if element["type"] == "node":
        lat = element.get("lat")
        lon = element.get("lon")
    else:
        center = element.get("center", {})
        lat = center.get("lat")
        lon = center.get("lon")
    return {
        "name": name,
        "latitude": lat,
        "longitude": lon,
        "tags": tags,
    }


def find_pubs_near_location(lat, lon, radius_m=1000, limit=5, timeout=15):
    query = f"""[out:json][timeout:{timeout}];
(
  node["amenity"="pub"](around:{radius_m},{lat},{lon});
  way["amenity"="pub"](around:{radius_m},{lat},{lon});
  relation["amenity"="pub"](around:{radius_m},{lat},{lon});
);
out center;"""

    last_error = None
    for endpoint in OVERPASS_URLS:
        try:
            response = requests.post(endpoint, data=query, timeout=timeout + 5)
            response.raise_for_status()
            data = response.json()
            break
        except requests.RequestException as exc:
            last_error = exc
            continue
    else:
        raise last_error or RuntimeError("Failed to query Overpass API")

    pubs = []
    for element in data.get("elements", []):
        pub = parse_overpass_element(element)
        if pub["latitude"] is None or pub["longitude"] is None:
            continue
        pub["distance_km"] = round(
            haversine_distance(lat, lon, pub["latitude"], pub["longitude"]), 1
        )
        pubs.append(pub)

    pubs.sort(key=lambda item: item["distance_km"])
    return pubs[:limit]
