"""
routes/trips.py

This module defines API endpoints related to trip planning.
Includes Flask routes for creating trips, retrieving trip details,
and managing trip-related actions such as selecting Costco gas
stations along a user's journey.

Blueprint: trips_bp
URL prefix: /api/trips
"""

#TODO: currentapp is temp!! just for polyline print testing
from flask import current_app, Blueprint, request, jsonify
from bson import ObjectId

from app.models.trip_model import create_trip, get_trip_by_id
from app.services.trip_service import no_stops_service, costco_stops_service

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


@trips_bp.route('/calculate-trip-no-stops', methods=['POST'])
def calculate_trip_no_stops():
    # Get trip_id json object from a string-based trip ID
    data = request.json
    trip_id = data.get('trip_id')
    if not trip_id:
        return jsonify({"error": "trip_id is required"}), 400

    # Using the trip_id object, calculate the route
    trip = no_stops_service(trip_id)
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

# (NEW) Costco-optimized trip route
"""
Costco-optimized trip calculation (adds refueling stops based on car range).
Expected JSON body:
{ "trip_id": "..." }
"""
@trips_bp.route('/calculate-trip-costco-stops', methods=['POST'])
def calculate_trip_costco_stops():

    data = request.get_json()
    trip_id = data.get('trip_id')

    if not trip_id:
        return jsonify({"error": "Missing trip_id"}), 400

    trip = costco_stops_service(trip_id)
    if trip:
        return jsonify({"message": "Trip with Costco stops calculated successfully"}), 200
    else:
        return jsonify({"error": "Trip with Costco stops calculation failed"}), 400


@trips_bp.route('/test-polyline', methods=['GET'])
def get_test_polyline():
    trips_collection = current_app.db.trips

    # Example: Fetch a trip by a specific trip_id you want to test
    test_trip_id = "680d297ee95e478132c0492f"  # <-- REPLACE this with the trip you want to test
    
    trip = trips_collection.find_one({"_id": ObjectId(test_trip_id)})

    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    polyline = trip.get("google_polyline")
    if not polyline:
        return jsonify({"error": "No polyline found in trip"}), 404

    return jsonify({"polyline": polyline})