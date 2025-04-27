"""
trip_service.py
----------------------------
Description: Handles the logic for trips, including route calculation and MongoDB updates.

"""

import polyline

# Model Imports
from app.models.trip_model import get_trip_by_id, update_trip_polyline, update_trip_waypoints, update_trip_google_maps_url
from app.models.user_model import get_user_by_id 
from app.models.station_model import get_all_stations  # (you might already have this)

# Service Imports
from app.services.google_maps_service import get_route_from_google

# Util Imports
from app.utils.spatial import haversine_distance

# ------------------ Simple trip calculation ------------------
def no_stops_service(trip_id):
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

# ------------------ Costco-optimized trip calculation ------------------

def costco_stops_service(trip_id):
    """
    Calculates a Costco-optimized trip plan based on user's car range.
    """
    # 1. Get trip and user info
    trip = get_trip_by_id(trip_id)
    if not trip:
        print(f"[ERROR] Trip ID {trip_id} not found in database.")
        return None

    user = get_user_by_id(trip["user_id"])
    if not user:
        print(f"[ERROR] User ID {trip['user_id']} not found in database.")
        return None

    origin = trip['origin']  # [lat, lng]
    destination = trip['destination']  # [lat, lng]
    mpg = user["mpg"]
    tank_size = user["tank_size"]
    buffer_percent = user["fuel_buffer_percent"]

    # Calculate effective range
    car_range = mpg * tank_size
    effective_range = car_range * ((100 - buffer_percent) * 0.01)

    print(f"[INFO] Effective car range with buffer: {effective_range:.2f} miles")

    # 2. Fetch direct route
    google_response = get_route_from_google(origin, destination)
    if not google_response or google_response.get('status') != "OK":
        print(f"[ERROR] Google Maps API Error: {google_response.get('status')}")
        print(f"[DETAILS] Full Google Response: {google_response}")
        return None

    # 3. Decode the route polyline into points
    encoded_polyline = google_response['routes'][0]['overview_polyline']['points']
    polyline_points = decode_polyline(encoded_polyline)

    if not polyline_points:
        print(f"[ERROR] Could not decode polyline for trip {trip_id}")
        return None

    # 4. Find Costco stops along the route
    costco_stops = find_gas_stops_along_route(polyline_points, effective_range)
    if not costco_stops:
        print(f"[INFO] No Costco stops needed for this trip.")
        costco_stops = []  # Still handle no stops case cleanly

    # 5. Requery Google with waypoints
    google_requery = get_route_from_google(origin, destination, costco_stops)
    if not google_requery or google_requery.get('status') != "OK":
        print(f"[ERROR] Google Maps API Requery Error: {google_requery.get('status')}")
        print(f"[DETAILS] Full Google Response: {google_requery}")
        return None

    updated_polyline = google_requery['routes'][0]['overview_polyline']['points']

    # 6. Save updated polyline and waypoints to DB
    success_polyline = update_trip_polyline(trip_id, updated_polyline)
    success_waypoints = update_trip_waypoints(trip_id, costco_stops)

    if not success_polyline or not success_waypoints:
        print(f"[ERROR] Failed to update trip {trip_id} with new Costco stops.")
        return None

    # 7. Save a prebuilt Google Maps URL
    update_trip_google_maps_url(trip_id, origin, destination, costco_stops)

    print(f"[SUCCESS] Trip {trip_id} updated with Costco-optimized route.")
    return get_trip_by_id(trip_id)


# ------------------ Find Nearby Costco ------------------

def find_nearby_costco(location, max_distance_miles=10):
    """
    Finds Costco stations near a given (lat, lng) location within a certain radius.
    """
    curr_loc_lat, curr_loc_lng = location
    stations = get_all_stations()
    reachable = []

    for station in stations:
        distance_to_station = haversine_distance(
            curr_loc_lat, curr_loc_lng,
            float(station['lat']), float(station['lng'])
        )

        if distance_to_station <= max_distance_miles:
            reachable.append({
                "station": station,
                "distance": distance_to_station
            })

    reachable.sort(key=lambda x: x['distance'])
    return reachable


# ------------------ Plan Gas Stops Along Route ------------------

def find_gas_stops_along_route(polyline_points, effective_range_miles):
    """
    Walks along the route until car range limit is reached,
    then searches backwards if no station is found nearby.
    """
    stops = []
    distance_traveled = 0
    search_backward_steps = 10
    search_radius_miles = 10

    i = 1
    while i < len(polyline_points):
        prev_point = polyline_points[i-1]
        current_point = polyline_points[i]

        prev_lat, prev_lng = prev_point
        curr_lat, curr_lng = current_point

        segment_distance = haversine_distance(prev_lat, prev_lng, curr_lat, curr_lng)
        distance_traveled += segment_distance
        print(f"[INFO] Moving by: {segment_distance:.2f} miles. Total traveled: {distance_traveled:.2f} miles.")

        if distance_traveled >= effective_range_miles:
            print(f"[INFO] Car range limit reached near point {i}. Searching for Costco nearby...")

            # Try finding a station at the current point first
            nearby_stations = find_nearby_costco(current_point, max_distance_miles=search_radius_miles)
            found_station = None
            found_at_index = i  # Default to current index

            # If no station found, search backwards
            if not nearby_stations:
                print(f"[INFO] No Costco found at current point. Searching backwards up to {search_backward_steps} steps...")
                for back_step in range(1, search_backward_steps + 1):
                    back_index = i - back_step
                    if back_index <= 0:
                        break
                    back_point = polyline_points[back_index]
                    nearby_stations = find_nearby_costco(back_point, max_distance_miles=search_radius_miles)
                    if nearby_stations:
                        print(f"[INFO] Found Costco {back_step} steps back.")
                        found_station = nearby_stations[0]['station']
                        found_at_index = back_index  # Save where we found it
                        break
            else:
                found_station = nearby_stations[0]['station']

            if found_station:
                stops.append((float(found_station['lat']), float(found_station['lng'])))
                print(f"[INFO] Costco gas station found: {found_station['name']}")
                distance_traveled = 0  # Reset after refueling

                # Move forward after the found stop
                i = found_at_index + 1
                continue
            else:
                print(f"[WARNING] No Costco found within search radius after range limit! Proceeding carefully...")

        i += 1

    return stops

def decode_polyline(encoded_polyline):
    return polyline.decode(encoded_polyline)
