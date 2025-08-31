# main.py (Final Corrected Version)
import os
from etl import extract_odds_data, transform_data, load_data, setup_database
from google.cloud import secretmanager


def run_etl_pipeline(event, context):
    """
    This is the entry point for the Cloud Function.
    It orchestrates the ETL process and prints a QA summary.
    """
    print("Starting ETL pipeline...")

    # --- Initialize clients and get secrets ---
    try:
        client = secretmanager.SecretManagerServiceClient()
        # TYPO FIX: Corrected project_id from 'sports-odds_etl-project'
        project_id = "sports-odds-etl-project"
        secret_id = "ODDS_API_KEY"
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

        response = client.access_secret_version(request={"name": name})
        os.environ['API_KEY'] = response.payload.data.decode("UTF-8")
        print("API Key successfully loaded.")
    except Exception as e:
        print(f"Error loading API Key from Secret Manager: {e}")
        return 'Failed to load API Key', 500
    # -----------------------------------------

    conn = setup_database()
    raw_games_data = extract_odds_data()

    if raw_games_data:
        clean_games_data, skipped_games_data = transform_data(raw_games_data)

        load_data(clean_games_data, conn)
        conn.close()

        # --- Generate and print the QA Summary Report ---
        print("\n--- ETL Run Summary ---")
        print(f"Records Received from API: {len(raw_games_data)}")
        print(f"Records Passing Validation: {len(clean_games_data)}")
        print(f"Records Skipped (e.g., missing odds): {len(skipped_games_data)}")
        print(f"Records Loaded to Database: {len(clean_games_data)}")
        print("-----------------------\n")

        print("ETL process completed successfully!")
        return 'Success'
    else:
        print("ETL process failed: No data extracted.")
        return 'Failure: No data extracted'