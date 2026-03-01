Smart Route Planner

Overview
Smart Route Planner is a Flask-based web application that calculates optimized driving routes between two locations. It compares alternative routes and provides information about distance, travel time, estimated CO2 emissions, accident risk estimate, and an overall route score. The application uses the OpenRouteService (ORS) API for geocoding, autocomplete, snapping, and routing.

Requirements

Python 3.9 or newer installed

Internet connection

An OpenRouteService (ORS) API key

How To Create an OpenRouteService Account and Get an API Key

Go to 

Click “Sign Up” and create a free account.

After verifying your email and logging in, go to the Dashboard.

Create a new API key.

Copy the generated API key.

Open app.py and replace: ORS_API_KEY = "YOUR_API_KEY_HERE" with your actual key inside the quotes. Save the file.

How To Run (First Time Setup)

Open Command Prompt.

Navigate to the project folder: cd path\to\smart-routing

Create a virtual environment: python -m venv venv

Activate the virtual environment (Windows): venv\Scripts\activate

Install required libraries: pip install -r requirements.txt

Run the application: python app.py

Open your browser and go to: 

How To Run After Initial Setup

Open Command Prompt.

Navigate to the project folder: cd path\to\smart-routing

Activate the virtual environment: venv\Scripts\activate

Run the application: python app.py

Open  in your browser

Troubleshooting
If you see errors about missing modules, run: pip install -r requirements.txt
If the virtual environment becomes corrupted, delete the venv folder and repeat the first time setup steps.
Ensure your ORS_API_KEY in app.py is valid and correctly pasted without extra spaces.
