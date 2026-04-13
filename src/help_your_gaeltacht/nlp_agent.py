"""Gemini-based NLP agent to parse natural language queries."""

import os
import json
import google.genai as genai
from google.genai import types

from help_your_gaeltacht.counties import get_county_coords, COUNTY_COORDS

# Configure with API key (use env var if set, otherwise use default)
api_key = os.getenv("GOOGLE_API_KEY", "your-api-key-here")
client = genai.Client(api_key=api_key)


def generate_with_fallback(contents, models=None, config=None):
    """Generate content with fallback models on quota errors."""
    if models is None:
        models = ['gemini-2.5-flash-lite', 'gemini-2.5-flash', 'gemini-2.0-flash']
    
    for model in models:
        try:
            if config:
                config.model = model
                response = client.models.generate_content(contents=contents, config=config)
            else:
                response = client.models.generate_content(model=model, contents=contents)
            return response
        except Exception as exc:
            if '429' in str(exc) or 'RESOURCE_EXHAUSTED' in str(exc):
                print(f"Model {model} quota exceeded, trying next model...")
                continue
            else:
                raise  # Re-raise non-quota errors
    
    raise Exception("All models have quota exceeded. Please try again later.")


def parse_query(user_input):
    """Use Gemini to parse natural language query and extract parameters."""
    
    county_options = ", ".join(sorted(set(v.split()[0] for v in COUNTY_COORDS.keys())))
    
    prompt = f"""You are a helpful assistant for Irish Gaeltacht information.

If the query is about finding Gaeltacht towns:
Available Irish counties: {county_options}

Extract:
1. COUNTY: The Irish county name (must be from the available list above)
2. LIMIT: Number of towns to find (default 5)
3. FIND_PUBS: true/false - should we search for pubs? (default false)
4. FIND_HERITAGE: true/false - should we search for heritage sites? (default false)
5. PUB_RADIUS: search radius for pubs in meters (default 1000)
6. HERITAGE_RADIUS: search radius for heritage in km (default 5)
7. FIND_VOLUNTEERS: true/false - should we search for volunteer opportunities? (default false)

Return JSON: {{"county": "...", "limit": 5, "find_pubs": false, "find_heritage": false, "pub_radius": 1000, "heritage_radius": 5, "find_volunteers": false}}

If the query is about searching for other information (like volunteers, events, projects, initiatives):
Return JSON: {{"search_query": "the search term"}}

User query: "{user_input}"

Return ONLY the JSON object, nothing else.
"""
    
    response = generate_with_fallback(prompt)
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


def search_info(query):
    """Use Gemini with Google Search to find information."""
    tools = [types.Tool(google_search=types.GoogleSearch())]
    config = types.GenerateContentConfig(tools=tools)
    
    search_prompt = f"Search the web for '{query}' and provide relevant, up-to-date information. Focus on Irish/Gaeltacht context if applicable. Summarize key findings."
    
    response = generate_with_fallback(contents=search_prompt, config=config)
    
    return response.candidates[0].content.parts[0].text.strip()


def process_natural_language_query(user_input):
    """Process a natural language query and return execution parameters."""
    try:
        params = parse_query(user_input)
    except Exception as exc:
        return {"error": f"Failed to parse query: {exc}"}
    
    # Check if it's a search query
    if "search_query" in params and params["search_query"]:
        return {"search_query": params["search_query"]}
    
    # Validate county for town search
    if not params.get("county"):
        return {"error": "No county found in query. Please mention an Irish county, like 'Galway' or 'Cork'."}
    
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
        "find_volunteers": params.get("find_volunteers", False),
        "pub_radius": max(500, params.get("pub_radius", 1000)),
        "heritage_radius": max(1, params.get("heritage_radius", 5)),
        "pub_limit": 3,
        "heritage_limit": 3,
    }
