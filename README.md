# Atlantec AI Challenge 2026
**State Machines** - Liam O Lionaird, Micael Pereira, Peter Hyland, Miguel Martins

## Project: Help Your Gaeltacht

A simple Gemini API-based CLI / Qt app that finds Gaeltacht towns in or near your county using open datasets. You can search further for local development projects and volunteering opportunities, and learn new Irish words and placenames.

### Our Datasets (found in `datasets` folder)
* [Gaeltacht Boundaries Generalised 100m](https://data.gov.ie/dataset/gaeltacht-boundaries-generalised-100m-national-administrative-boundaries-20151) (Published by Tailte Eireann, Creative Commons Attribution license)
* [Settlements Generalised 100m](https://data.gov.ie/dataset/settlements-generalised-100m-national-statistical-boundaries-20151) (Published by Tailte Eireann, Creative Commons Attribution license)
* `gael_towns.geojson`
    * Our custom list of Gaeltacht towns calculated from the above datasets using the `new_dataset.py` script in the `datasets` folder.

### How to Run:
Run the `interactive_agent.py` script in the `scripts` folder. The script will prompt you to enter a Gemini API key before launching.

Alternatively, you can try an experimental Qt GUI version of the app by running `qt_app.py` in the `scripts` folder.

* Type an Irish county name to search for Gaeltacht towns in or near that county.
* The agent will search for pubs and heritage sites in each town using OpenStreetMap if requested.
* If asked about volunteering work, the agent will run a Gemini API query for guidance on nearby opportunities.

This app was partially created using ChatGPT Codex.
