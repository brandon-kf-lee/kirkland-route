"""
trip_service.py
----------------------------
Description: Handles the logic for trips, including route calculation and MongoDB updates.

"""

from app.models.trip_model import get_trip_by_id, update_trip_polyline
from app.services.google_maps_service import get_route_from_google

# This module retrieves route documents, requests route data from Google Maps API, and stores the calculated path back into MongoDB.
def calculate_and_save_trip(trip_id):
    # 1. Get the route info from DB
    trip = get_trip_by_id(trip_id)
    if not trip:
        print(f"[ERROR] Trip ID {trip_id} not found in database.")
        return None

    origin = trip['origin']
    destination = trip['destination']

    # 2. Get path from Google
    google_response = get_route_from_google(origin, destination)

    if not google_response or google_response.get('status') != "OK":
        print(f"[ERROR] Google Maps API Error: {google_response.get('status')}")
        print(f"[DETAILS] Full Google Response: {google_response}")
        return None

    # 3. Extract path (overview_polyline or steps)
    overview_polyline = google_response["routes"][0]["overview_polyline"]["points"]

    # 4. Save it back into the route
    updated = update_trip_polyline(trip_id, overview_polyline)
    if not updated:
        print(f"[ERROR] Failed to update trip {trip_id} with polyline.")
        return None

    return get_trip_by_id(trip_id)
