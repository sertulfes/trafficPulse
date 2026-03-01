TrafficPulse
TrafficPulse is a Flask-based web application that compares multiple driving routes between two locations. It analyzes distance, travel time, estimated CO2 emissions, accident risk score, and overall route performance. The application uses the OpenRouteService (ORS) API for geocoding, autocomplete, road snapping, and alternative route generation.

Features
Multiple alternative driving routes

Distance and travel time comparison

Estimated CO2 emissions analysis

Accident risk scoring

Overall route performance scoring

Expandable turn-by-turn directions

Location autocomplete

Road snapping for accurate routing

Requirements
Python 3.9 or higher

Internet connection

OpenRouteService API key

Setting Up OpenRouteService API Key
Go to 

Create a free account

Verify your email and log in

Open the Dashboard

Generate a new API key

Open app.py

Replace: ORS_API_KEY = "YOUR_API_KEY_HERE"

Paste your key inside the quotes and save

First Time Setup
Open Command Prompt (Windows) or Terminal (Mac).

Navigate to the project folder:
cd path/to/smart-routing

Create a virtual environment:
python -m venv venv (Windows)
python3 -m venv venv (Mac)

Activate the virtual environment:
Windows: venv\Scripts\activate
Mac: source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the application:
Windows: python app.py
Mac: python3 app.py

Open your browser and go to:

Running After Initial Setup
Navigate to the project folder.

Activate the virtual environment.

Run python app.py (or python3 app.py on Mac).

Open  in your browser.

Troubleshooting
If you see a missing module error, run:
pip install -r requirements.txt

If the virtual environment becomes corrupted, delete the venv folder and repeat the First Time Setup steps.

Project Structure
app.py – Main Flask application

templates/ – HTML templates

requirements.txt – Python dependencies

README.md – Project documentation

TrafficPulse demonstrates API integration, backend route processing, frontend interactivity, and environmental impact modeling within a structured Flask application.