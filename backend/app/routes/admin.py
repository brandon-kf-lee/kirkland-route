"""
admin.py

This module defines administrative routes for manual operations, such as scraping Costco gas 
station data on demand. These routes are intended for developer or admin use and are not 
part of the regular user-facing API.

Routes:
- POST /api/admin/scrape-costco: Trigger a manual scrape of Costco gas stations near a preset location.

Blueprint: admin_bp
URL prefix: /api/admin
"""

from flask import Blueprint, jsonify, current_app
from app.services.costco_scraper import scrape_all_costco_stations, scrape_single_coordinate

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/scrape-costco', methods=['POST'])
def scrape_costco():
    scrape_all_costco_stations(current_app.db)
    return jsonify({"message": "Scraping finished!"})
