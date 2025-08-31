# NFL Sports Odds ETL Pipeline

## Description

This project is a complete ETL (Extract, Transform, Load) pipeline built with Python. It extracts upcoming NFL game odds from **The Odds API**, transforms the data to select key information, and loads it into a local **SQLite** database. The primary purpose is to create a historical dataset of betting odds to track line movements over time.

This project was built to demonstrate proficiency in data engineering fundamentals, API integration, data modeling, testing, and version control.

---

## Features

- **Extract**: Fetches data from a live, external REST API.
- **Transform**: Cleans and structures the raw JSON data into a relational format.
- **Load**: Stores the clean data in a local SQLite database, creating the table if it doesn't exist.
- **Testing**: Includes a unit test suite with `pytest` to ensure data transformation logic is correct.
- **Configuration**: Manages API keys securely using a `.env` file.
- **Code Quality**: Adheres to modern Python standards using a `.flake8` configuration and the `black` code formatter.

---

## Technologies Used

- **Language**: Python 3
- **Primary Libraries**:
  - `requests`: For making HTTP requests to the API.
  - `sqlite3`: For database interaction.
  - `python-dotenv`: For managing environment variables.
- **Testing**: `pytest`
- **Version Control**: Git & GitHub

---

## Setup and Installation

Follow these steps to run the project locally.

**1. Clone the repository:**
```bash
git clone [Your GitHub Repository URL]
cd sports_odds_etl
'''
2. Create and activate a virtual environment:

```bash
# For MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
'''
3. Install the required dependencies:

'''
pip install -r requirements.txt
'''
4. Set up your environment variables:
Create a file named .env in the root of the project directory and add your API key from The Odds API:

API_KEY=your_actual_api_key_here
Usage
To run the entire ETL pipeline, execute the main.py script from the root directory:

'''
python main.py
'''
After running, a odds.db file will be created (or updated) in the project directory containing the latest odds.