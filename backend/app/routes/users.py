from flask import Blueprint, request, jsonify
from app.models.user_model import save_user_profile
from app.models.user_model import save_user_profile, get_user_by_id, get_user_by_username


# Create Blueprint
users_bp = Blueprint('user', __name__)

@users_bp.route('/profile', methods=['POST'])
def save_profile():
    """
    Endpoint to save a user profile.
    Expects JSON data in the request body.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Attempt to save profile
        result = save_user_profile(data)

        if result:
            return jsonify({"message": "Profile saved successfully!"}), 200
        else:
            return jsonify({"error": "Failed to save profile"}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@users_bp.route('/profile/<username>', methods=['GET'])
def get_profile(username):
    """
    Endpoint to retrieve a user profile by username.
    """
    try:
        user = get_user_by_username(username) 

        if user:
            # Convert MongoDB ObjectId to string if necessary
            user['_id'] = str(user['_id'])
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
