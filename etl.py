# etl.py
import os
import requests
import sqlite3
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


# In etl.py

def transform_data(raw_data):
    """
    Transforms raw API data, separating valid records from skipped ones.

    Returns:
        tuple: A tuple containing two lists:
               - A list of clean game odds dictionaries (to be loaded).
               - A list of raw game data that was skipped due to validation issues.
    """
    clean_games = []
    skipped_games = []  # New list to track skipped records

    for game in raw_data:
        # Find the odds from our preferred bookmaker
        bookmaker_odds = next(
            (book for book in game['bookmakers'] if book['key'] == BOOKMAKER),
            None
        )

        # If bookmaker isn't found, the record is invalid for our purposes
        if not bookmaker_odds:
            skipped_games.append(game)
            continue  # Skip to the next game

        # Find home and away team prices
        outcomes = bookmaker_odds['markets'][0]['outcomes']
        home_price = next(
            (m['price'] for m in outcomes if m['name'] == game['home_team']),
            None
        )
        away_price = next(
            (m['price'] for m in outcomes if m['name'] == game['away_team']),
            None
        )

        # If both prices are found, the record is clean
        if home_price and away_price:
            clean_games.append({
                'id': game['id'],
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'commence_time': game['commence_time'],
                'home_team_odds': home_price,
                'away_team_odds': away_price
            })
        # Otherwise, the record is incomplete and should be skipped
        else:
            skipped_games.append(game)

    return clean_games, skipped_games


def setup_database():
    """Creates the game_odds table if it doesn't exist and returns a connection."""
    conn = sqlite3.connect(":memory:")  # Use an in-memory DB for simplicity
    conn.execute('''
        CREATE TABLE IF NOT EXISTS game_odds (
            id TEXT PRIMARY KEY,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            commence_time TEXT NOT NULL,
            home_team_odds REAL NOT NULL,
            away_team_odds REAL NOT NULL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    print("In-memory database setup complete.")
    return conn


def load_data(transformed_data, conn):  # Corrected function name
    """Loads the transformed game odds into the given database connection."""
    if not transformed_data:
        print("No data to load.")
        return

    cursor = conn.cursor()

    for game in transformed_data:
        cursor.execute('''
            INSERT OR IGNORE INTO game_odds (
                id, home_team, away_team, commence_time,
                home_team_odds, away_team_odds
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            game['id'], game['home_team'], game['away_team'],
            game['commence_time'], game['home_team_odds'],
            game['away_team_odds']
        ))

    conn.commit()
    print(f"Successfully loaded or ignored {len(transformed_data)} records.")