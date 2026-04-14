"""
Generates new dataset containing Gaeltacht-only towns.
Author: Liam Ó Lionáird
"""

import geopandas

with open("Gaeltacht_Boundaries_Generalised_100m.geojson") as gaeltacht_json, open("Settlements_Generalised_100m.geojson") as towns_json:
    gaeltacht = geopandas.read_file(gaeltacht_json).to_crs(4326)
    towns = geopandas.read_file(towns_json).to_crs(4326)

gael_towns = towns.loc[towns.within(gaeltacht.union_all())]

gael_towns.to_file("gael_towns.geojson")