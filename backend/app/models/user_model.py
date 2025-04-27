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

def save_user_profile(data):
    """
    Save a new user profile to the database.
    If the user already exists (based on _id), update their profile instead.
    """
    users_collection = current_app.db.users
    try:
        # If data contains '_id', attempt to update existing user
        if '_id' in data:
            user_id = data['_id']
            if isinstance(user_id, str):
                user_id = ObjectId(user_id)  # Convert to ObjectId if needed

            update_result = users_collection.update_one(
                {'_id': user_id},
                {'$set': data}
            )

            if update_result.modified_count > 0:
                print(f"[INFO] Updated user")
                return True
            else:
                print("[INFO] No changes made to the user.")
                return False

        else:
            # Insert as new document
            insert_result = users_collection.insert_one(data)
            if insert_result.inserted_id:
                print(f"[INFO] Inserted new user with ID {insert_result.inserted_id}")
                return True
            else:
                return False

    except Exception as e:
        print(f"[ERROR] Failed to save user profile: {e}")
        return False

def get_user_by_username(username):
    users_collection = current_app.db.users
    try:
        return users_collection.find_one({'username': username})
    except Exception as e:
        print(f"[ERROR] Could not retrieve user by username: {e}")
        return None