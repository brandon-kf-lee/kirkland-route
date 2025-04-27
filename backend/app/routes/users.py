from flask import Blueprint, request, jsonify
from app.models.user_model import save_user_profile  # assume you have a model function

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
