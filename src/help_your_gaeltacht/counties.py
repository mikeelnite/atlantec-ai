"""Irish county center coordinates for quick lookups."""

COUNTY_COORDS = {
    "carlow": (52.4247, -6.9271),
    "cavan": (53.9879, -7.3606),
    "clare": (52.8317, -9.0937),
    "cork": (51.8985, -8.4625),
    "donegal": (55.0196, -8.1093),
    "dublin": (53.3498, -6.2603),
    "dun laoghaire": (53.2765, -6.1392),
    "dún laoghaire": (53.2765, -6.1392),
    "fingal": (53.4386, -6.1671),
    "galway": (53.2707, -9.0568),
    "galway city": (53.2707, -9.0568),
    "kerry": (52.0091, -9.5399),
    "kildare": (53.1640, -6.8057),
    "kilkenny": (52.5089, -7.2519),
    "laois": (52.8986, -7.2639),
    "leitrim": (54.2667, -8.0167),
    "limerick": (52.6393, -8.6267),
    "longford": (53.7324, -7.7924),
    "louth": (53.9999, -6.4308),
    "mayo": (54.0667, -9.2500),
    "meath": (53.6470, -6.7847),
    "monaghan": (54.2487, -6.8167),
    "offaly": (53.2518, -7.6550),
    "roscommon": (53.6127, -8.2018),
    "sligo": (54.2674, -8.4765),
    "tipperary": (52.5045, -7.5620),
    "tyrone": (54.6165, -7.1522),
    "waterford": (52.2557, -7.5898),
    "westmeath": (53.5316, -7.6447),
    "wexford": (52.3344, -6.4637),
    "wicklow": (52.9864, -6.2595),
}


def get_county_coords(county_name):
    """Look up approximate center coordinates for an Irish county."""
    normalized = county_name.strip().lower()
    if normalized.startswith("county "):
        normalized = normalized[len("county "):].strip()
    if normalized in COUNTY_COORDS:
        return COUNTY_COORDS[normalized]
    raise ValueError(
        f"County '{county_name}' not recognized. Available: {', '.join(sorted(set(v.split()[0] for v in COUNTY_COORDS.keys())))}"
    )
