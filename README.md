TrafficPulse
TrafficPulse is a Flask-based web application that compares multiple driving routes between two Canadian locations. It analyzes distance, travel time, estimated CO2 emissions, and overall route performance. The app uses the OpenRouteService (ORS) API for geocoding, autocomplete, road snapping, and route generation.

Enter a start and end location to receive 1–3 route options depending on trip distance. Each route displays travel time, distance, emissions data, percentage difference in CO2 compared to the most efficient route, and a performance score. Click any route to expand full turn‑by‑turn driving instructions.

Features
Multiple alternative routes (short trips)

Distance and travel time comparison

Estimated CO2 emissions analysis

Emissions percentage comparison

Dynamic route performance scoring

Expandable turn-by-turn directions

Location autocomplete

Road snapping for improved routing accuracy

Requirements
Python 3.9 or higher

Internet connection

OpenRouteService API key

Setting Up Your OpenRouteService API Key
Go to 

Create a free account

Verify your email and log in

Open the Dashboard

Generate a new API key

Open app.py

Replace the ORS_API_KEY value with your key

Save the file

How to Run (Automatic Setup)
TrafficPulse includes a run.py file that automatically:

Creates a virtual environment if one does not exist

Installs all dependencies from requirements.txt

Starts the Flask application

To Run:
Open Command Prompt (Windows) or Terminal (Mac)

Navigate to the project folder:

cd path/to/TrafficPulse

Run:

Windows: python run.py
Mac: python3 run.py

Open your browser and go to:


That’s it. No manual virtual environment setup or pip installation required.

Running Again Later
Simply navigate to the project folder and run:

Windows: python run.py
Mac: python3 run.py

The script will reuse the existing virtual environment.

Troubleshooting
If Python is not recognized, ensure Python is installed and added to PATH.

If routing fails, confirm your ORS API key is valid and has remaining usage quota.

If you encounter persistent dependency issues, delete the venv folder and run python run.py again.

Project Structure
run.py – Automatic setup and launcher

app.py – Main Flask backend logic

templates/ – HTML templates

requirements.txt – Python dependencies

README.md – Project documentation

TrafficPulse demonstrates API integration, backend route analytics, environmental impact modeling, and interactive route comparison within a structured Flask application.
