"""
routes/trips.py

This module defines API endpoints related to trip planning.
Includes Flask routes for creating trips, retrieving trip details,
and managing trip-related actions such as selecting Costco gas
stations along a user's journey.

Blueprint: trips_bp
URL prefix: /api/trips
"""

from flask import Blueprint, request, jsonify
from app.models.trip_model import create_trip

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/plan', methods=['POST'])
def plan_trip():
    trip_data = request.json
    trip_id = create_trip(trip_data)
    return jsonify({"trip_id": trip_id}), 201