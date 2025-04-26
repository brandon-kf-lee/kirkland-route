"""
models/trip_model.py

This module handles all database operations related to trip planning.
Includes functions to create new trips and retrieve trip details from MongoDB.

Collection: trips
"""

from flask import current_app

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
    return trips_collection.find_one({"_id": trip_id})


