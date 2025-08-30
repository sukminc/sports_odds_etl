# main.py
from etl import extract_odds_data

if __name__ == "__main__":
    games_data = extract_odds_data()

    if games_data:
        print(f"Successfully fetched {len(games_data)} upcoming games.")
        # Print the details of the first game to see the structure
        if len(games_data) > 0:
            print("\n--- Example Game Data ---")
            print(games_data[0])
            print("-------------------------\n")
    else:
        print("Could not fetch game data.")