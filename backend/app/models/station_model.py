"""
models/station_model.py

This module handles all database operations related to Costco gas stations.
Includes functions to retrieve station details from MongoDB.

Collection: stations
"""

from flask import current_app

"""
Retrieve all Costco gas station documents from the stations collection.
"""
def get_all_stations():
    stations_collection = current_app.db.stations
    return list(stations_collection.find({}))
