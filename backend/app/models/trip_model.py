"""
models/trip_model.py

This module handles all database operations related to trip planning.
Includes functions to create new trips and retrieve trip details from MongoDB.

Collection: trips
"""

from flask import current_app
from bson import ObjectId

def create_trip(trip_data):
    """
    Insert a new trip document into the trips collection.
    """
    trips_collection = current_app.db.trips
    result = trips_collection.insert_one(trip_data)
    return str(result.inserted_id)

def get_trip_by_id(trip_id):
    """
    Retrieve a trip document from the trips collection by its ID.
    """
    trips_collection = current_app.db.trips
    return trips_collection.find_one({"_id": ObjectId(trip_id)})


def update_trip_polyline(trip_id, polyline):
    """
    Update the trip document with the Google Maps polyline path.
    """
    trips_collection = current_app.db.trips

    result = trips_collection.update_one(
        {"_id": ObjectId(trip_id)},
        {"$set": {"google_polyline": polyline}}
    )
    
    print(f"[DEBUG] Matched Count: {result.matched_count}")
    print(f"[DEBUG] Modified Count: {result.modified_count}")
    
    return result.modified_count > 0