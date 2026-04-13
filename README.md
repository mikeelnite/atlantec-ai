# Help Your Gaeltacht

A small Python project to help find the nearest Gaeltacht towns from your location and generate a basic Irish vocabulary glossary.

## What it does

- Loads Gaeltacht town data from the local GeoJSON file generated in the dataset archive
- Finds the nearest Gaeltacht towns for a given latitude/longitude
- Builds a simple Irish-English glossary from town names

## Setup

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. The local datasets are already imported under `datasets/`:
- `datasets/gael_towns.geojson`
- `datasets/Gaeltacht_Boundaries_Generalised_100m.geojson`
- `datasets/Settlements_Generalised_100m.geojson`

3. Set your Google Gemini API key (required for AI features):

```bash
# On Windows PowerShell:
$env:GEMINI_API_KEY = "your-api-key-here"

# On Linux/macOS:
export GEMINI_API_KEY=your-api-key-here
```

Or set it permanently in your system environment variables.

4. Run the interactive AI agent:

```bash
python scripts/interactive_agent.py
```

Try queries like:
- "Find towns in Galway"
- "Find volunteer opportunities in Mayo Gaeltacht towns"
- "Irish language learning resources"

5. Run the CLI:

4. To look up pubs near each returned town:

```bash
python scripts/find_nearest.py --lat 53.2707 --lon -9.0568 --limit 5 --find-pubs
```

> Pub lookup uses OpenStreetMap's Overpass API. If one endpoint is busy or rate-limited, the script will try alternate public Overpass endpoints.

## Notes

- The original source archive was imported from `C:\Users\migue\Downloads\atlantec-ai-challenge-main.zip`.
- To regenerate `gael_towns.geojson`, run `scripts/new_dataset.py` from the local dataset folder after installing `geopandas`.
- If you want to query remote ArcGIS GeoService endpoints instead of local files, update `src/help_your_gaeltacht/data_loader.py`.
