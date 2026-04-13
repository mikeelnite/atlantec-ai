"""Gemini-based NLP agent to parse natural language queries."""

import os
import json
import google.genai as genai

from help_your_gaeltacht.counties import get_county_coords, COUNTY_COORDS

# Configure with API key (use env var if set, otherwise use default)
api_key = os.getenv("GOOGLE_API_KEY", "your-api-key-here")
client = genai.Client(api_key=api_key)


def parse_query(user_input):
    """Use Gemini to parse natural language query and extract parameters."""
    
    county_options = ", ".join(sorted(set(v.split()[0] for v in COUNTY_COORDS.keys())))
    
    prompt = f"""You are a helpful assistant parsing queries about Irish Gaeltacht towns, pubs, and heritage sites.

Available Irish counties: {county_options}

Parse this user query and extract:
1. COUNTY: The Irish county name (must be from the available list above)
2. LIMIT: Number of towns to find (default 5)
3. FIND_PUBS: true/false - should we search for pubs? (default false)
4. FIND_HERITAGE: true/false - should we search for heritage sites? (default false)
5. PUB_RADIUS: search radius for pubs in meters (default 1000)
6. HERITAGE_RADIUS: search radius for heritage in km (default 5)

User query: "{user_input}"

Return ONLY a JSON object with these keys, nothing else:
{{"county": "...", "limit": 5, "find_pubs": false, "find_heritage": false, "pub_radius": 1000, "heritage_radius": 5}}
"""
    
    response = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    response_text = response.candidates[0].content.parts[0].text.strip()
    
    # Extract JSON from response
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            raise ValueError(f"Could not parse Gemini response: {response_text}")
    
    return result


def process_natural_language_query(user_input):
    """Process a natural language query and return execution parameters."""
    try:
        params = parse_query(user_input)
    except Exception as exc:
        return {"error": f"Failed to parse query: {exc}"}
    
    # Validate county
    if not params.get("county"):
        return {"error": "No county found in query. Please mention an Irish county."}
    
    try:
        lat, lon = get_county_coords(params["county"])
    except ValueError as exc:
        return {"error": str(exc)}
    
    return {
        "county": params["county"],
        "lat": lat,
        "lon": lon,
        "limit": max(1, min(params.get("limit", 5), 10)),
        "find_pubs": params.get("find_pubs", False),
        "find_heritage": params.get("find_heritage", False),
        "pub_radius": max(500, params.get("pub_radius", 1000)),
        "heritage_radius": max(1, params.get("heritage_radius", 5)),
        "pub_limit": 3,
        "heritage_limit": 3,
    }
