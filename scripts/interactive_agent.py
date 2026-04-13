#!/usr/bin/env python
"""Interactive NLP agent CLI for Help Your Gaeltacht."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from help_your_gaeltacht.data_loader import load_custom_town_list
from help_your_gaeltacht.nearest_towns import find_nearest_towns
from help_your_gaeltacht.glossary import generate_glossary
from help_your_gaeltacht.poi import find_pubs_near_location
from help_your_gaeltacht.heritage import query_heritage_assets
from help_your_gaeltacht.nlp_agent import process_natural_language_query


def main():
    print("=" * 60)
    print("Help Your Gaeltacht - AI Agent")
    print("=" * 60)
    print("\nTry natural language queries like:")
    print('  "Find towns in Galway"')
    print('  "Show me Gaeltacht towns in Cork with pubs nearby"')
    print('  "I want to visit Clare and see heritage sites"')
    print('  "Mayo Gaeltacht towns, please list 3"')
    print("\nType 'quit' or 'exit' to leave.\n")

    dataset_path = ROOT / "datasets" / "gael_towns.geojson"
    features = load_custom_town_list(dataset_path)

    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Parse natural language query
        params = process_natural_language_query(user_input)

        if "error" in params:
            print(f"Agent: Error — {params['error']}\n")
            continue

        # Execute search
        try:
            nearest = find_nearest_towns(
                features,
                (params["lat"], params["lon"]),
                limit=params["limit"],
            )

            if not nearest:
                print(f"Agent: No Gaeltacht towns found near {params['county']}.\n")
                continue

            print(
                f"Agent: Found {len(nearest)} Gaeltacht town(s) near {params['county']}:\n"
            )
            for town in nearest:
                print(f"  • {town['name']} ({town['distance_km']} km)")

                if params["find_pubs"]:
                    try:
                        pubs = find_pubs_near_location(
                            town["latitude"],
                            town["longitude"],
                            radius_m=params["pub_radius"],
                            limit=params["pub_limit"],
                        )
                        if pubs:
                            print(f"    Pubs:")
                            for pub in pubs:
                                print(f"      - {pub['name']} ({pub['distance_km']} km)")
                        else:
                            print(f"    No pubs found nearby")
                    except Exception as exc:
                        print(f"    Pub search: {exc}")

                if params["find_heritage"]:
                    try:
                        heritage = query_heritage_assets(
                            town["latitude"],
                            town["longitude"],
                            radius_km=params["heritage_radius"],
                            limit=params["heritage_limit"],
                        )
                        if heritage:
                            print(f"    Heritage sites:")
                            for site in heritage:
                                print(f"      - {site['name']} ({site['distance_km']} km)")
                        else:
                            print(f"    No heritage sites found nearby")
                    except Exception as exc:
                        print(f"    Heritage search: {exc}")

            glossary = generate_glossary(nearest)
            if glossary:
                print(f"\n  Irish words to learn:")
                for irish, english in glossary.items():
                    print(f"    {irish} = {english}")

        except Exception as exc:
            print(f"Agent: Error during search — {exc}\n")

        print()


if __name__ == "__main__":
    main()
