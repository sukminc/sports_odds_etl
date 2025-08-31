# local_runner.py
from main import run_etl_pipeline
import os
from dotenv import load_dotenv

# --- IMPORTANT ---
# This local runner needs to load the .env file because it's not
# running in the cloud context where the environment variable is set.
print("Loading environment variables from .env file for local run...")
load_dotenv()

# We need to manually set the API_KEY environment variable for the ETL script to find.
# The code in main.py is for the cloud; this is the local equivalent.
if 'API_KEY' not in os.environ:
    print("API_KEY not found in environment. Ensure your .env file is correct.")
else:
    print("API_KEY loaded. Running ETL pipeline locally...")
    # Call the function just like the cloud would
    run_etl_pipeline(None, None)