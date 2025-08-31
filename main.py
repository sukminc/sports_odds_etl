# main.py (Final Robust Version)
import os
from etl import extract_odds_data, transform_data, load_data, setup_database
from google.cloud import secretmanager


def run_etl_pipeline(event, context):
    """
    This is the entry point function for the Cloud Function.
    It orchestrates the ETL process.
    """
    print("Starting ETL pipeline...")

    # --- Best Practice: Initialize clients and get secrets inside the function ---
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = "sports-odds-etl-project"
        secret_id = "ODDS_API_KEY"
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        
        # Access the secret version.
        response = client.access_secret_version(request={"name": name})
        
        # Set the secret as an environment variable for the ETL script to use.
        os.environ['API_KEY'] = response.payload.data.decode("UTF-8")
        print("API Key successfully loaded from Secret Manager.")
    except Exception as e:
        print(f"Error loading API Key from Secret Manager: {e}")
        # Fail loudly if we can't get the key.
        return 'Failed to load API Key', 500
    # ------------------------------------------------------------------------

    # We use an in-memory database for this simple cloud function.
    conn = setup_database()

    raw_games_data = extract_odds_data()

    if raw_games_data:
        clean_games_data = transform_data(raw_games_data)
        load_data(clean_games_data, conn)
        conn.close()  # Close the connection when done
        print("ETL process completed successfully!")
        return 'Success'
    else:
        print("ETL process failed: No data extracted.")
        return 'Failure: No data extracted'