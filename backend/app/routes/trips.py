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
from app.models.trip_model import create_trip, get_trip_by_id
from app.services.trip_service import calculate_and_save_trip

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/plan', methods=['POST'])
def plan_trip():
    trip_data = request.json
    trip_id = create_trip(trip_data)
    return jsonify({"trip_id": trip_id}), 201

# TODO: Redundant?
@trips_bp.route('/<trip_id>', methods=['GET'])
def fetch_trip(trip_id):
    trip = get_trip_by_id(trip_id)
    if trip:
        trip['_id'] = str(trip['_id'])  # MongoDB _id needs to be converted to string
        return jsonify(trip), 200
    else:
        return jsonify({"error": "Trip not found"}), 404
    
@trips_bp.route('/calculate_trip', methods=['POST'])
def calculate_trip():
    # Get trip_id json object from a string-based trip ID
    data = request.json
    trip_id = data.get('trip_id')
    if not trip_id:
        return jsonify({"error": "trip_id is required"}), 400

    # Using the trip_id object, calculate the route
    trip = calculate_and_save_trip(trip_id)
    if not trip:
        return jsonify({"error": "Failed to calculate trip route"}), 500

    # Return the successful trip calculation
    return jsonify({
        "message": "Trip calculated successfully",
        "trip": {
            "id": str(trip['_id']),
            "origin": trip['origin'],
            "destination": trip['destination'],
            "polyline": trip['google_polyline']
        }
    })