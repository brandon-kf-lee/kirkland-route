from flask import Flask
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # MongoDB setup
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    app.db = client["kirkland_route_db"]

    # Import and register blueprints
    from app.routes.admin import admin_bp
    from app.routes.trips import trips_bp
    #from app.routes.stations import stations_bp

    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(trips_bp, url_prefix='/api/trips')
    #app.register_blueprint(stations_bp, url_prefix='/api/stations')
    

    return app
