# main.py
import os
from datetime import datetime, timezone
from google.cloud import secretmanager
from google.cloud import storage

# --- Our ETL functions ---
# Note the import change here!
from etl import extract_odds_data, transform_data, load_data_to_csv_string

# --- Configuration ---
# TODO: IMPORTANT! Replace this with the actual name of your GCS bucket.
GCS_BUCKET_NAME = "your-gcs-bucket-name-here"


def run_etl_pipeline(event, context):
    """
    This is the entry point for the Cloud Function.
    It orchestrates the ETL process and uploads the result to GCS.
    """
    print("Starting ETL pipeline...")

    # --- Step 0: Get API Key from Secret Manager ---
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = "sports-odds-etl-project"
        secret_id = "ODDS_API_KEY"
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

        response = client.access_secret_version(request={"name": name})
        os.environ['API_KEY'] = response.payload.data.decode("UTF-8")
        print("API Key successfully loaded from Secret Manager.")
    except Exception as e:
        print(f"Error loading API Key from Secret Manager: {e}")
        return 'Failed to load API Key', 500
    # --- Step 1: EXTRACT ---
    raw_games_data = extract_odds_data()

    if not raw_games_data:
        print("ETL process failed: No data extracted from API.")
        return 'Failure: No data extracted'

    # --- Step 2: TRANSFORM ---
    clean_games_data, skipped_games_data = transform_data(raw_games_data)

    # --- Step 3: LOAD ---
    # First, convert the clean data to a CSV string.
    csv_data_string = load_data_to_csv_string(clean_games_data)
    # Now, upload that string to Google Cloud Storage.
    if csv_data_string:
        try:
            # Create a client to interact with GCS
            storage_client = storage.Client()
            # Get the bucket object
            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            # Define a unique filename using the current UTC timestamp
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%S')
            filename = f"odds_data/{timestamp}.csv"
            # Create a new blob (file) and upload the data
            blob = bucket.blob(filename)
            blob.upload_from_string(csv_data_string, content_type='text/csv')
            print(f"Success! File '{filename}' uploaded to bucket '{GCS_BUCKET_NAME}'.")

        except Exception as e:
            print(f"Error uploading file to GCS: {e}")
            return 'Failed to upload data', 500

    # --- Generate and print the QA Summary Report ---
    print("\n--- ETL Run Summary ---")
    print(f"Records Received from API: {len(raw_games_data)}")
    print(f"Records Passing Validation: {len(clean_games_data)}")
    print(f"Records Skipped: {len(skipped_games_data)}")
    print(f"Records Uploaded to GCS: {len(clean_games_data)}")  # Changed this line
    print("-----------------------\n")

    print("ETL process completed successfully!")
    return 'Success'