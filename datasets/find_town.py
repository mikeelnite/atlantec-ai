"""
Script to calculate nearest Gaeltacht towns using our `gael_towns` dataset.
Author: Liam Ó Lionáird
"""

import geopandas
from shapely import Point

if __name__ == "__main__":
    # More robust geocoding goes here. For now, choose from the below sample towns as input.
    # Sample town lat/long coordinates from Wikipedia
    sample_towns = geopandas.GeoDataFrame(
        index=["Kilkenny", "Galway", "Cork", "Letterkenny"],
        data={
            "geometry": [
                Point(-7.251389, 52.650556),
                Point(-9.048889, 53.271944),
                Point(-8.47, 51.897222),
                Point(-7.7203, 54.9566),
            ]
        },
        crs=4326,
    ).to_crs(2157)

    with open("datasets/gael_towns.geojson") as gaeltacht_json:
        gaeltacht = geopandas.read_file(gaeltacht_json).to_crs(2157)

    your_town = input("Enter your town.\n> ")

    closest_towns = [
        gaeltacht.distance(sample_towns.loc[your_town],align=True).sort_values().index[x]
        for x in range(3)
    ]

    print(f"""The 3 closest Gaeltacht towns are:
    {gaeltacht.loc[closest_towns[0]]["SETTL_NAME"]}
    {gaeltacht.loc[closest_towns[1]]["SETTL_NAME"]}
    {gaeltacht.loc[closest_towns[2]]["SETTL_NAME"]}""")
