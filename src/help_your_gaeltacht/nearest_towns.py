import math


def haversine_distance(lat1, lon1, lat2, lon2):
    radius_km = 6371.0
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def centroid_from_geometry(geometry):
    coords = geometry.get("coordinates")
    if not coords:
        return None, None

    points = []
    geom_type = geometry.get("type")
    if geom_type == "Point":
        return coords[1], coords[0]
    if geom_type == "Polygon":
        rings = coords
    elif geom_type == "MultiPolygon":
        rings = [ring for polygon in coords for ring in polygon]
    else:
        return None, None

    for ring in rings:
        for pt in ring:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                points.append(pt)

    if not points:
        return None, None

    lon = sum(pt[0] for pt in points) / len(points)
    lat = sum(pt[1] for pt in points) / len(points)
    return lat, lon


def extract_town_info(feature):
    props = feature.get("properties", {})
    geometry = feature.get("geometry", {})
    lat, lon = centroid_from_geometry(geometry)
    return {
        "name": props.get("SETTL_NAME") or props.get("SETTLEMENT") or props.get("NAME") or props.get("name") or props.get("Town") or props.get("town_name") or "Unknown",
        "description": props.get("DESCRIPTION") or props.get("description") or "",
        "latitude": lat,
        "longitude": lon,
        "properties": props,
    }


def find_nearest_towns(features, location, limit=5, max_distance_km=None):
    lat, lon = location
    towns = []
    for feature in features:
        town = extract_town_info(feature)
        if town["latitude"] is None or town["longitude"] is None:
            continue
        distance = haversine_distance(lat, lon, town["latitude"], town["longitude"])
        if max_distance_km is not None and distance > max_distance_km:
            continue
        town["distance_km"] = round(distance, 1)
        towns.append(town)
    towns.sort(key=lambda item: item["distance_km"])
    return towns[:limit]
