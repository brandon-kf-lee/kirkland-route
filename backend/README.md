# File Structure
```
backend/
├── venv/                 # Python virtual environment
├── app/                  # Main backend app
│   ├── __init__.py        # App factory, Flask setup
│   ├── routes/            # All your API endpoint, blueprints (HTTP requests from frontend)
│   │   ├── __init__.py
│   │   ├── trips.py       # Trip planning routes (origin/destination, routes, stops)
│   │   ├── stations.py    # Costco gas station endpoints
│   │   └── users.py       # User management if needed
│   ├── models/            # MongoDB schemas (DB requests from backend services)
│   │   ├── __init__.py
│   │   ├── trip_model.py
│   │   ├── station_model.py
│   │   └── user_model.py
│   ├── services/          # Utility functions (scraping, route calculation, emissions calc, etc.)
│   │   ├── __init__.py
│   │   ├── google_maps_service.py
│   │   └── scraper_service.py
│   ├── config.py          # App configuration (Mongo URI, API keys loaded from .env)
│   └── utils.py           # Small helper functions
├── .env                   # Secret keys and config (DO NOT COMMIT)
├── requirements.txt       # List of Python packages
├── run.py                 # Entry point to run the Flask app
└── README.md              # Quick explanation of backend setup
```