import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from help_your_gaeltacht.data_loader import load_custom_town_list
from help_your_gaeltacht.nearest_towns import find_nearest_towns
from help_your_gaeltacht.glossary import generate_glossary
from help_your_gaeltacht.poi import find_pubs_near_location
from help_your_gaeltacht.heritage import query_heritage_assets
from help_your_gaeltacht.counties import get_county_coords


def main():
    parser = argparse.ArgumentParser(description="Find nearest Gaeltacht towns from your location.")
    parser.add_argument("--county", type=str, help="Irish county name (e.g., Galway, Cork, Dublin)")
    parser.add_argument("--lat", type=float, help="Latitude of the search location")
    parser.add_argument("--lon", type=float, help="Longitude of the search location")
    parser.add_argument("--limit", type=int, default=5, help="Number of nearest towns to return")
    parser.add_argument("--max-distance", type=float, default=None, help="Maximum search radius in kilometers")
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent.parent / "datasets" / "gael_towns.geojson", help="Path to the Gaeltacht towns GeoJSON file")
    parser.add_argument("--find-pubs", action="store_true", help="Search for pubs near each returned town using OpenStreetMap")
    parser.add_argument("--pub-radius", type=int, default=1000, help="Search radius for pubs in meters")
    parser.add_argument("--pub-limit", type=int, default=3, help="Maximum number of pubs to list per town")
    parser.add_argument("--find-heritage", action="store_true", help="Search for heritage assets near each returned town using data.gov.ie")
    parser.add_argument("--heritage-radius", type=float, default=5, help="Search radius for heritage assets in kilometers")
    parser.add_argument("--heritage-limit", type=int, default=3, help="Maximum number of heritage assets to list per town")
    args = parser.parse_args()

    # Determine search location from county or coordinates
    if args.county:
        try:
            lat, lon = get_county_coords(args.county)
        except ValueError as exc:
            print(f"Error: {exc}")
            return
    elif args.lat is not None and args.lon is not None:
        lat, lon = args.lat, args.lon
    else:
        print("Error: provide either --county or both --lat and --lon")
        return

    features = load_custom_town_list(args.dataset)
    nearest = find_nearest_towns(features, (lat, lon), limit=args.limit, max_distance_km=args.max_distance)

    if not nearest:
        print("No nearby Gaeltacht towns found.")
        return

    location_str = args.county if args.county else f"({lat}, {lon})"
    print(f"Nearest Gaeltacht towns to {location_str}:\n")
    for town in nearest:
        print(f"- {town['name']} ({town['distance_km']} km)")
        if town.get("description"):
            print(f"  {town['description']}")
        if args.find_pubs:
            try:
                pubs = find_pubs_near_location(
                    town["latitude"],
                    town["longitude"],
                    radius_m=args.pub_radius,
                    limit=args.pub_limit,
                )
            except Exception as exc:
                print(f"  Pub search failed: {exc}")
            else:
                if pubs:
                    print("  Pubs nearby:")
                    for pub in pubs:
                        print(f"    - {pub['name']} ({pub['distance_km']} km)")
                else:
                    print(f"  No pubs found within {args.pub_radius} m")
        if args.find_heritage:
            try:
                heritage = query_heritage_assets(
                    town["latitude"],
                    town["longitude"],
                    radius_km=args.heritage_radius,
                    limit=args.heritage_limit,
                )
            except Exception as exc:
                print(f"  Heritage search failed: {exc}")
            else:
                if heritage:
                    print("  Heritage assets nearby:")
                    for asset in heritage:
                        print(f"    - {asset['name']} ({asset['distance_km']} km)")
                        if asset.get("type"):
                            print(f"      Type: {asset['type']}")
                else:
                    print(f"  No heritage assets found within {args.heritage_radius} km")

    glossary = generate_glossary(nearest)
    if glossary.get("terms"):
        print("\nIrish words from nearby town names:")
        for irish, english in glossary["terms"]:
            print(f"- {irish}: {english}")

    if glossary.get("expressions"):
        print("\nUseful Irish expressions:")
        for irish, english in glossary["expressions"]:
            print(f"- {irish}: {english}")


if __name__ == "__main__":
    main()
