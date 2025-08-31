# etl.py
import os
import requests
import csv
import io
from dotenv import load_dotenv

# --- CONSTANTS ---
load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.the-odds-api.com/v4/sports"
SPORT = "americanfootball_nfl"
REGIONS = "us"
MARKETS = "h2h"
BOOKMAKER = "draftkings"


def extract_odds_data():
    """Extracts NFL moneyline odds from The Odds API."""
    url = f"{BASE_URL}/{SPORT}/odds"
    params = {'apiKey': API_KEY, 'regions': REGIONS, 'markets': MARKETS}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print("API Request successful!")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An other error occurred: {err}")
    return []


def transform_data(raw_data):
    """
    Transforms raw API data, separating valid records from skipped ones.

    Returns:
        tuple: A tuple containing two lists:
               - A list of clean game odds dictionaries (to be loaded).
               - A list of raw game data that was skipped due to validation issues.
    """
    clean_games = []
    skipped_games = []

    for game in raw_data:
        bookmaker_odds = next(
            (book for book in game['bookmakers'] if book['key'] == BOOKMAKER),
            None
        )

        if not bookmaker_odds:
            skipped_games.append(game)
            continue

        outcomes = bookmaker_odds['markets'][0]['outcomes']
        home_price = next(
            (m['price'] for m in outcomes if m['name'] == game['home_team']),
            None
        )
        away_price = next(
            (m['price'] for m in outcomes if m['name'] == game['away_team']),
            None
        )

        if home_price and away_price:
            clean_games.append({
                'id': game['id'],
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'commence_time': game['commence_time'],
                'home_team_odds': home_price,
                'away_team_odds': away_price
            })
        else:
            skipped_games.append(game)

    return clean_games, skipped_games


def load_data_to_csv_string(transformed_data):
    """
    Takes a list of dictionaries and converts it into a CSV formatted string.

    Returns:
        str: A string containing the data in CSV format, or None if no data.
    """
    if not transformed_data:
        print("No transformed data to format.")
        return None

    # Use io.StringIO to create an in-memory text file
    output = io.StringIO()

    # Define the headers based on the dictionary keys
    headers = [
        'id', 'home_team', 'away_team', 'commence_time',
        'home_team_odds', 'away_team_odds'
    ]
    writer = csv.DictWriter(output, fieldnames=headers)

    # Write the header and the rows to our in-memory file
    writer.writeheader()
    writer.writerows(transformed_data)

    print(f"Successfully formatted {len(transformed_data)} records into a CSV string.")

    # Get the string value from the in-memory file
    return output.getvalue()