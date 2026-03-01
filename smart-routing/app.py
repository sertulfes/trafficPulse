import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

ORS_API_KEY = "YOUR_API_KEY_HERE"


# --------------------------------------------------
# AUTOCOMPLETE
# --------------------------------------------------
@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q")

    if not query or len(query) < 2:
        return jsonify([])

    url = "https://api.openrouteservice.org/geocode/autocomplete"

    headers = {"Authorization": ORS_API_KEY}

    params = {
        "text": query,
        "boundary.country": "CA",
        "size": 5
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    suggestions = []

    if "features" in data:
        for feature in data["features"]:
            suggestions.append({
                "label": feature["properties"]["label"],
                "coords": feature["geometry"]["coordinates"]
            })

    return jsonify(suggestions)


# --------------------------------------------------
# SNAP
# --------------------------------------------------
def snap_multiple(coords_list):
    url = "https://api.openrouteservice.org/v2/snap/driving-car"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "locations": coords_list,
        "radius": 5000
    }

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    snapped = []

    if "locations" in data:
        for i, loc in enumerate(data["locations"]):
            if loc and "location" in loc:
                snapped.append(loc["location"])
            else:
                snapped.append(coords_list[i])
    else:
        return coords_list

    return snapped


# --------------------------------------------------
# ROUTING
# --------------------------------------------------
def get_routes(start_coords, end_coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [start_coords, end_coords],
        "alternative_routes": {
            "target_count": 3,
            "share_factor": 0.6
        }
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()


# --------------------------------------------------
# MAIN ROUTE HANDLER
# --------------------------------------------------
@app.route("/route", methods=["POST"])
def route():

    start_coords = list(map(float, request.form["start_coords"].split(",")))
    end_coords = list(map(float, request.form["end_coords"].split(",")))

    start_coords, end_coords = snap_multiple([start_coords, end_coords])

    data = get_routes(start_coords, end_coords)

    if "routes" not in data:
        return render_template("index.html", error="Routing failed.")

    routes_output = []

    # First calculate all CO2 to compare later
    all_co2 = []

    for route in data["routes"]:
        distance_km = route["summary"]["distance"] / 1000
        co2 = distance_km * 0.22
        all_co2.append(co2)

    best_co2 = min(all_co2)

    for i, route in enumerate(data["routes"]):

        summary = route["summary"]
        steps = route["segments"][0]["steps"]

        distance_km = summary["distance"] / 1000
        duration_min = summary["duration"] / 60

        co2 = all_co2[i]
        risk = distance_km * 0.02

        # CO2 comparison
        co2_diff = co2 - best_co2
        co2_percent = ((co2_diff) / best_co2) * 100 if best_co2 != 0 else 0

        score = 100 - (duration_min * 0.5 + co2 * 0.3 + risk * 0.2)

        routes_output.append({
            "route_number": i + 1,
            "distance_km": round(distance_km, 2),
            "travel_time_min": round(duration_min, 2),
            "co2_kg": round(co2, 2),
            "risk_score": round(risk, 2),
            "overall_score": round(score, 2),
            "co2_diff": round(co2_diff, 2),
            "co2_percent": round(co2_percent, 1),
            "steps": steps
        })

    return render_template("index.html", routes=routes_output)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)