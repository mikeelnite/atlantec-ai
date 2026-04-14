# Atlantec AI Challenge 2026
**State Machines** - Liam O Lionaird, Micael Pereira, Peter Hyland, Miguel Martins

**Note:** This is a fork of our original repo at [liam-ol/atlantec-ai-challenge](https://github.com/liam-ol/atlantec-ai-challenge), additional Git history can be viewed there.

## Project: Help Your Gaeltacht

A simple Gemini API-based app that finds Gaeltacht towns in or near your county using open datasets. You can search further for local places of interest and volunteering opportunities, and learn new Irish words and placenames.

To suit the needs of every user, a variety of UI frontends are available: a command-line interface, a Qt desktop app, and a web app.

### Our Datasets (found in `datasets` folder)
* [Gaeltacht Boundaries Generalised 100m](https://data.gov.ie/dataset/gaeltacht-boundaries-generalised-100m-national-administrative-boundaries-20151) (Published by Tailte Eireann, Creative Commons Attribution license)
* [Settlements Generalised 100m](https://data.gov.ie/dataset/settlements-generalised-100m-national-statistical-boundaries-20151) (Published by Tailte Eireann, Creative Commons Attribution license)
* `gael_towns.geojson`
    * Our custom list of Gaeltacht towns calculated from the above datasets using the `new_dataset.py` script in the `datasets` folder.

### How to Run:
Ensure all Python libraries in `requirements.txt` are installed.

1. **CLI:** Run the `interactive_agent.py` script in the `scripts` folder. The script will prompt you to enter a Gemini API key before launching.

2. **Qt GUI:** Run `qt_app.py` in the `scripts` folder.

3. **Web App:** Follow instructions in the `webapp` folder's `README` to host the web app locally.

Once you're up and running:

* Type an Irish county name to search for Gaeltacht towns in or near that county.
* The agent will search for pubs and heritage sites in each town using OpenStreetMap if requested.
* If asked about volunteering work, the agent will run a Gemini API query for guidance on nearby opportunities.

This app was created with coding assistance from ChatGPT Codex and Bolt.
