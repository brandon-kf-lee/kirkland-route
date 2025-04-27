"""
google_maps_service.py
----------------------------
Description: Exclusively provides functions to interact with the Google Maps Directions API.

"""

import requests
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# This module fetches route data from the Google Maps API based on provided origin and destination points.
def get_route_from_google(origin, destination, waypoints=None):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin}",
        "destination": f"{destination}",
        "mode": "driving",
        "key": GOOGLE_API_KEY
    }
    
    # If there are waypoints, update the request with them
    if waypoints:
        waypoints_str = "optimize:true|" + "|".join(f"{lat},{lng}" for lat, lng in waypoints)
        params["waypoints"] = waypoints_str

    print("[DEBUG] Params sent to Google:", params)

    response = requests.get(base_url, params=params, timeout=10)

    print(f"[DEBUG] Google API response status: {response.status_code}")
    # print(f"[DEBUG] Google API response content: {response.text}")

    if response.status_code == 200:
        return response.json()
    else:
        return None