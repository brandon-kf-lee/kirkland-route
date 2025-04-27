"""
models/trip_model.py

This module handles all database operations related to trip planning.
Includes functions to create new trips and retrieve trip details from MongoDB.

Collection: trips
"""

from flask import current_app
from bson import ObjectId
from urllib.parse import quote

def create_trip(origin, destination, user_id=None):
    """
    Create and insert a new trip document into the database.
    """
    trips_collection = current_app.db.trips

    trip_data = {
        'origin': origin,               # Expected to be [lat, lng]
        'destination': destination,     # Expected to be [lat, lng]
        'user_id': ObjectId(user_id),    
    }

    result = trips_collection.insert_one(trip_data)
    return result.inserted_id
def get_trip_by_id(trip_id):
    """
    Retrieve a trip document from the trips collection by its ID.
    """
    trips_collection = current_app.db.trips
    try:
        return trips_collection.find_one({"_id": ObjectId(trip_id)})
    except Exception as e:
        print(f"[ERROR] Could not retrieve user: {e}")
        return None


def update_trip_polyline(trip_id, polyline):
    """
    Update the trip document with the Google Maps polyline path.
    """
    trips_collection = current_app.db.trips

    result = trips_collection.update_one(
        {"_id": ObjectId(trip_id)},
        {"$set": {"google_polyline": polyline}}
    )

    find = get_trip_by_id(trip_id)
    return result.modified_count > 0


def update_trip_waypoints(trip_id, waypoints):
    """
    Update the trip document with the list of Costco gas station waypoints.
    """
    trips_collection = current_app.db.trips

    result = trips_collection.update_one(
        {"_id": ObjectId(trip_id)},
        {"$set": {"waypoints": waypoints}}
    )

    return result.modified_count > 0

def update_trip_google_maps_url(trip_id, origin, destination, waypoints):
    """
    Update trip with a ready-to-use Google Maps URL for navigation.
    """
    trips_collection = current_app.db.trips
    origin_str = f"{origin}"
    destination_str = f"{destination}"
    waypoints_str = "|".join(f"{lat},{lng}" for lat, lng in waypoints)

    base_url = "https://www.google.com/maps/dir/?api=1"
    maps_url = f"{base_url}&origin={quote(origin_str)}&destination={quote(destination_str)}&waypoints={quote(waypoints_str)}"

    trips_collection.update_one(
        {"_id": ObjectId(trip_id)},
        {"$set": {"google_maps_url": maps_url}}
    )

def update_trip_stats(trip_id, stats_data):
    """Update trip statistics for a trip in the database.

    Args:
        trip_id (str): ID of the trip to update.
        stats_data (dict): Dictionary containing updated trip stats.
    """

    trips_collection = current_app.db.trips
    result = trips_collection.update_one(
        {"_id": ObjectId(trip_id)},
        {"$set": {"stats": stats_data}}
    )
    if result.matched_count == 0:
        print(f"[ERROR] No trip found with ID {trip_id} to update stats.")
    else:
        print(f"[INFO] Trip stats updated for trip {trip_id}.")