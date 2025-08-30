# etl.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONSTANTS ---
API_KEY = os.getenv('API_KEY')
# API endpoint for in-season sports
BASE_URL = "https://api.the-odds-api.com/v4/sports"
# The sport we are interested in
SPORT = "americanfootball_nfl"
# The region for the odds
REGIONS = "us"
# The market we want odds for (h2h is moneyline)
MARKETS = "h2h"
# The sportsbook we want odds from
BOOKMAKER = "draftkings"

def extract_odds_data():
    """
    Extracts NFL moneyline odds from The Odds API for a specific bookmaker.

    Returns:
        list: A list of dictionaries, where each dictionary is a game with odds.
              Returns an empty list if the request fails.
    """
    # Construct the full URL
    url = f"{BASE_URL}/{SPORT}/odds"
    
    # Parameters for the API request
    params = {
        'apiKey': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
    }

    try:
        response = requests.get(url, params=params)
        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        print("API Request successful!")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except Exception as err:
        print(f"An other error occurred: {err}")
    
    return []