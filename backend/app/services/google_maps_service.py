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
def get_route_from_google(origin, destination):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
