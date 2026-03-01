import requests
from flask import Flask, request, render_template, jsonify
import math

app = Flask(__name__)

ORS_API_KEY = "YOUR_API_KEY_HERE"

# --------------------------------------------------
# HAVERSINE
# --------------------------------------------------
def haversine(coord1, coord2):
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


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

    if "locations" not in data:
        return coords_list

    snapped = []

    for i, loc in enumerate(data["locations"]):
        if loc and "location" in loc:
            snapped.append(loc["location"])
        else:
            snapped.append(coords_list[i])

    return snapped


# --------------------------------------------------
# ROUTES
# --------------------------------------------------
def get_routes(start_coords, end_coords):

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    approx_distance = haversine(start_coords, end_coords)

    if approx_distance <= 120:
        body = {
            "coordinates": [start_coords, end_coords],
            "alternative_routes": {
                "target_count": 3,
                "share_factor": 0.6
            }
        }
    else:
        body = {
            "coordinates": [start_coords, end_coords]
        }

    response = requests.post(url, json=body, headers=headers)
    return response.json()


# --------------------------------------------------
# SCORING
# --------------------------------------------------
def calculate_score(duration_min, distance_km, co2,
                    durations, co2_list):

    # MULTIPLE ROUTES → relative scoring
    if len(durations) > 1:

        best_duration = min(durations)
        worst_duration = max(durations)

        best_co2 = min(co2_list)
        worst_co2 = max(co2_list)

        def normalize(value, best, worst):
            if worst == best:
                return 1
            return (worst - value) / (worst - best)

        duration_score = normalize(duration_min, best_duration, worst_duration)
        co2_score = normalize(co2, best_co2, worst_co2)

        score = duration_score * 60 + co2_score * 40
        return round(score, 1)

    # SINGLE ROUTE → efficiency based
    else:
        if distance_km == 0:
            return 0

        time_per_km = duration_min / distance_km
        expected_time_per_km = 1.1

        efficiency = expected_time_per_km / time_per_km
        score = efficiency * 85

        return max(50, min(90, round(score, 1)))


# --------------------------------------------------
# MAIN ROUTE
# --------------------------------------------------
@app.route("/route", methods=["POST"])
def route():

    try:
        start_coords = list(map(float, request.form["start_coords"].split(",")))
        end_coords = list(map(float, request.form["end_coords"].split(",")))
    except:
        return render_template("index.html", routes=None, error="Invalid location.")

    start_coords, end_coords = snap_multiple([start_coords, end_coords])
    data = get_routes(start_coords, end_coords)

    if "routes" not in data:
        return render_template("index.html", routes=None, error="Routing failed.")

    routes_output = []
    durations = []
    co2_list = []

    # FIRST PASS
    for route_data in data["routes"]:
        distance_km = route_data["summary"]["distance"] / 1000
        duration_min = route_data["summary"]["duration"] / 60
        co2 = distance_km * 0.21

        durations.append(duration_min)
        co2_list.append(co2)

    best_co2 = min(co2_list)

    # SECOND PASS
    for i, route_data in enumerate(data["routes"]):

        summary = route_data["summary"]
        steps = route_data["segments"][0]["steps"]

        distance_km = summary["distance"] / 1000
        duration_min = summary["duration"] / 60
        co2 = co2_list[i]

        score = calculate_score(
            duration_min,
            distance_km,
            co2,
            durations,
            co2_list
        )

        co2_diff = co2 - best_co2
        co2_percent = (co2_diff / best_co2 * 100) if best_co2 != 0 else 0

        routes_output.append({
            "route_number": i + 1,
            "distance_km": round(distance_km, 2),
            "travel_time_min": round(duration_min, 2),
            "co2_kg": round(co2, 3),
            "co2_diff": round(co2_diff, 3),
            "co2_percent": round(co2_percent, 2),
            "overall_score": score,
            "steps": steps
        })

    return render_template("index.html", routes=routes_output, error=None)


@app.route("/")
def home():
    return render_template("index.html", routes=None, error=None)


if __name__ == "__main__":
    app.run(debug=True)