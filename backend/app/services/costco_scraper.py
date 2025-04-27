"""
services/costco_scraper.py
Inspired by: apsun's gastrak (https://github.com/apsun/gastrak)

This module provides functionality to scrape Costco gas station data using Costco's internal Ajax 
API endpoint. It mimics realistic browser traffic to avoid detection, leveraging session cookies and 
Chrome-like headers.

Features:
- Fetch warehouses near a specific coordinate (latitude, longitude).
- Scrape an entire geographic region by stepping through a lat/lng grid.
- Only updates MongoDB records if existing warehouse data is older than a defined freshness threshold (default 6 hours).
- Randomized request timing to rate-limit and avoid server-side scraping detection.
- All scraped data is stored or updated in a MongoDB 'stations' collection.

Environment Variables:
- COSTCO_COOKIE: Session cookie string required to authenticate API requests.

"""

import requests
import time
import random
from dotenv import load_dotenv
import os

load_dotenv()

# Costco API endpoint
COSTCO_API_URL = "https://www.costco.com/AjaxWarehouseBrowseLookupView"

# Define freshness threshold before next scrape/DB update
FRESHNESS_THRESHOLD_SECONDS = 6 * 60 * 60  # 6 hours = 21600 seconds

# United States Bounding Boxes
LAT_STEP = 2.0    # Latitude step
LNG_STEP = 2.0    # Longitude step

# US
US_LAT_START = 24.523096    # Southernmost point (Florida Keys)
US_LAT_END = 49.384358      # Northernmost point (Minnesota)
US_LNG_START = -124.409591  # Westernmost point (California)
US_LNG_END = -66.949895     # Easternmost point (Maine)

# West, states included: WA, OR, CA, ID, MT, WY, NV, UT, CO, AZ, NM
W_LAT_START = 31.332177    # Southern Arizona/NM/CA
W_LAT_END = 49.002494      # Northern Washington
W_LNG_START = -124.763068  # Western Washington
W_LNG_END = -102.041524    # Eastern Colorado

#Midwest, states included: ND, SD, NE, KS, MN, IA, MO, WI, IL, IN, MI, OH
MW_LAT_START = 36.970298    # Southern Missouri
MW_LAT_END = 49.384358      # Northern Minnesota
MW_LNG_START = -104.057698  # Western North Dakota/South Dakota
MW_LNG_END = -80.518693     # Eastern Ohio

#South, states included: TX, OK, AR, LA, KY, TN, MS, AL, WV, VA, NC, SC, GA, FL, MD, DE, DC
S_LAT_START = 24.523096    # Southern Florida
S_LAT_END = 39.147458      # Northern Kentucky/Virginia
S_LNG_START = -106.645646  # Western Texas
S_LNG_END = -75.048939     # Eastern Delaware

# Northeast
NE_LAT_START = 38.451013    # Southern Delaware
NE_LAT_END = 47.459686      # Northern Maine
NE_LNG_START = -80.519891   # Western Pennsylvania
NE_LNG_END = -66.949895     # Eastern Maine

# De-duplication based on warehouse ID
seen_ids = set()

# Headers to mimic browser
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-NZ,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "origin": "https://www.costco.com",
    "referer": "https://www.costco.com/",
    "cookie": os.getenv('COSTCO_COOKIE')
}

# Use a Session
session = requests.Session()
session.headers.update(HEADERS)

"""
Fetch a list of Costco warehouses with gas stations near a specific latitude and longitude.
Raises an exception if the HTTP request fails.
"""
def fetch_warehouses_near(lat, lng):
    params = {
        "numOfWarehouses": "50",
        "hasGas": "true",
        "populateWarehouseDetails": "true",
        "latitude": str(lat),
        "longitude": str(lng),
        "countryCode": "US",
    }
    try:
        response = requests.get(COSTCO_API_URL, headers=HEADERS, params=params, timeout=30)

        # Only try JSON if 200 OK
        if response.status_code == 200:
            response.raise_for_status()
            return response.json()
        else:
            print("Unexpected status, skipping...")

    except requests.exceptions.RequestException as e:
        print(f"Skipping ({lat}, {lng}): {e}")
        return None

"""
Safely parse a price string to a float.
Returns None if price is invalid or missing.
"""
def safe_parse_price(price):
    try:
        return float(price)
    except (TypeError, ValueError):
        return None
    
"""
Process an individual warehouse's data and upsert (update or insert) it into MongoDB.
If a warehouse already exists, its record will be updated with the latest gas prices and timestamp.
"""
def process_and_store_warehouse(stations_collection, warehouse):
    stloc_id = int(warehouse.get('stlocID'))
    gas_prices = warehouse.get('gasPrices', {})

    # Check if this warehouse already exists
    existing = stations_collection.find_one({"stlocID": stloc_id})
    
    # If it exists, check timestamp
    if existing:
        last_update_time = existing.get("timestamp", 0)
        current_time = time.time()

        # If last update was within the freshness window, skip update
        if (current_time - last_update_time) < FRESHNESS_THRESHOLD_SECONDS:
            print(f"Skipped warehouse {stloc_id} - {existing.get('name', 'Unknown')} (fresh, updated recently)")
            return

    # Otherwise, proceed to update
    data = {
        "timestamp": time.time(),
        "stlocID": stloc_id,
        "name": warehouse.get('locationName'),
        "lat": warehouse.get('latitude'),
        "lng": warehouse.get('longitude'),
        "price_diesel": safe_parse_price(gas_prices.get('diesel')),
        "price_regular": safe_parse_price(gas_prices.get('regular')),
        "price_premium": safe_parse_price(gas_prices.get('premium')),
    }

    stations_collection.update_one(
        {"stlocID": stloc_id},   # Match on warehouse id
        {"$set": data},          # Set (update) with new data
        upsert=True              # Insert if not exists
    )
    print(f"Inserted/updated warehouse: {stloc_id} - {data['name']}")
    


# ---------------------- Scraping Main Functions ----------------------
"""
Scrape Costco gas station data across a wide grid of the US and Canada.
Insert or update each warehouse into the MongoDB 'stations' collection.
Rate-limits requests randomly to avoid being blocked by Costco servers.
"""
def scrape_all_costco_stations(db):
    stations_collection = db['stations']
    stations_collection.create_index("stlocID", unique=True)
    warehouse_count = 0

    lat = W_LAT_START
    while lat <= W_LAT_END:
        lng = W_LNG_START
        while lng <= W_LNG_END:
            try:
                print(f"Fetching warehouses near ({lat}, {lng})...")
                warehouses = fetch_warehouses_near(lat, lng)
                
                if not warehouses:
                    lng += LNG_STEP
                    continue  # Skip this point if fetch failed

                # Costco's weird API: warehouses start at index 1
                for warehouse in warehouses[1:]:
                    process_and_store_warehouse(stations_collection, warehouse)
            except Exception as e:
                print(f"Error fetching ({lat}, {lng}): {e}")

            # Rate limiting
            time.sleep(random.uniform(1.5, 10.5))  # Wait between 1.5–10.5 seconds randomly to mimic human behaviour

            lng += LNG_STEP
        lat += LAT_STEP

    print(f"Finished scraping. {warehouse_count} warehouses updated or inserted.")
    warehouse_count += 1

"""
Scrape Costco warehouses near a specific single coordinate (latitude, longitude).
"""
def scrape_single_coordinate(db, lat, lng):

    stations_collection = db['stations']
    stations_collection.create_index("stlocID", unique=True)

    print(f"Fetching warehouses near ({lat}, {lng})...")

    warehouses = fetch_warehouses_near(lat, lng)

    if not warehouses:
        print(f"No warehouses found near ({lat}, {lng}) or request failed.")
        return

    for warehouse in warehouses[1:]:  # Skip the weird [0] entry
        process_and_store_warehouse(stations_collection, warehouse)

    print(f"Finished scraping coordinate ({lat}, {lng}).")