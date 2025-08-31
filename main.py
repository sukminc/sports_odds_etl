# main.py
from etl import extract_odds_data, transform_data, load_data, setup_database

if __name__ == "__main__":
    # 1. Ensure the database and table exist
    setup_database()
    
    # 2. EXTRACT raw data from the API
    raw_games_data = extract_odds_data()

    if raw_games_data:
        # 3. TRANSFORM the data into a clean format
        clean_games_data = transform_data(raw_games_data)
        
        # 4. LOAD the clean data into our database
        load_data(clean_games_data)
        
        print("\nETL process completed successfully!")
    else:
        print("ETL process failed: No data extracted.")