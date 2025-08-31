# NFL Sports Odds ETL Pipeline

## Description

This project is a complete ETL (Extract, Transform, Load) pipeline built with Python and deployed to Google Cloud Platform. It extracts upcoming NFL game odds from **The Odds API**, transforms the data to select key information, and loads it into a database. The primary purpose is to create a historical dataset of betting odds to track line movements over time.

This project was built to demonstrate proficiency in data engineering fundamentals, API integration, cloud deployment, automated testing, and version control.

---

## Features

- **Extract**: Fetches data from a live, external REST API.
- **Transform**: Cleans and structures the raw JSON data into a relational format.
- **Load**: Stores the clean data in an in-memory SQLite database upon execution.
- **Cloud Deployment**: The entire ETL process is deployed as a serverless **Google Cloud Function**.
- **Security**: Manages the API key securely in the cloud using **Google Secret Manager** and IAM permissions.
- **Testing**: Includes a unit test suite with `pytest` to ensure data transformation logic is correct.
- **Code Quality**: Adheres to modern Python standards using a `.flake8` configuration.

---

## Technologies Used

- **Language**: Python 3.12
- **Cloud Platform**: Google Cloud Platform (GCP)
  - **Compute**: Cloud Functions (1st Gen)
  - **Security**: Secret Manager, IAM
  - **Deployment**: gcloud CLI
- **Primary Libraries**:
  - `requests`: For making HTTP requests to the API.
  - `sqlite3`: For database interaction.
  - `google-cloud-secret-manager`: For secure API key handling.
- **Testing**: `pytest`
- **Version Control**: Git & GitHub

---

## Setup and Installation

Follow these steps to run the project locally.

**1. Clone the repository:**
```bash
git clone [Your GitHub Repository URL]
cd sports_odds_etl
```
**2. Create and activate a virtual environment:**

```
# For MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```
**3. Install the required dependencies:**

```
pip install -r requirements.txt
```
**4. Set up your environment variables:**
Create a file named .env in the root of the project directory and add your API key from The Odds API:
```
API_KEY=your_actual_api_key_here
```
Usage

Local Execution

To run the pipeline on your local machine, use the local_runner.py script. This script simulates the execution environment and uses the .env file for the API key.

```
python local_runner.py
Cloud Execution
```
The pipeline is deployed as an HTTP-triggered Google Cloud Function. To run the live version, send a POST request to its trigger URL.

```
curl -X POST https://us-central1-sports-odds-etl-project.cloudfunctions.net/run-etl-pipeline
```
