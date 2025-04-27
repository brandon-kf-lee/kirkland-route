"""
user_model.py
----------------------------
Description: Handles database operations related to users.

"""

from bson import ObjectId
from flask import current_app


def get_user_by_id(user_id):
    """
    Retrieve a user document by its ID.
    """
    users_collection = current_app.db.users
    try:
        return users_collection.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        print(f"[ERROR] Could not retrieve user: {e}")
        return None
