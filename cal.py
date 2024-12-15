import requests
import sqlite3
from datetime import datetime


# API Key and Configuration
CALENDAR_API_KEY = "mEqFBnqUJrid9qOl3seOq8gyYFlPSPyx"
DATABASE_NAME = "holidays.db"
COUNTRY_CODE = "US" 
state = "Michigan"
city = "Ann Arbor"
YEAR = 2024  
month = 9 
location = "us-mi"
limit = 25 


def fetch_holidays(api_key, country, year):
    """
    Fetch holiday data from the Calendarific API.

    Args:
        api_key (str): API key for Calendarific.
        country (str): Country code (e.g., "US").
        year (int): Year for which to fetch holidays.

    Returns:
        list: A list of holiday dictionaries.
    """
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": api_key,
        "country": country,
        "year": year,
        "month": month,
        "location": location,

    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("response", {}).get("holidays", [])
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def filter_holidays_by_date(holidays, start_date, end_date):
    """
    Filter holidays within a specific date range.

    Args:
        holidays (list): List of holiday dictionaries.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        list: Filtered list of holiday dictionaries.
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    filtered_holidays = [
        holiday for holiday in holidays
        if start_date_obj <= datetime.strptime(holiday["date"]["iso"], "%Y-%m-%d") <= end_date_obj
    ]

    return filtered_holidays

def initialize_database(db_name):
    """
    Create or initialize the SQLite database.

    Args:
        db_name (str): Name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the holidays table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            country TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def store_holidays_in_db(holidays, db_name):
    """
    Store holiday data into the SQLite database.

    Args:
        holidays (list): List of holiday dictionaries.
        db_name (str): Name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for holiday in holidays:
        cursor.execute('''
            INSERT INTO holidays (name, description, country, date)
            VALUES (?, ?, ?, ?)
        ''', (
            holiday["name"],
            holiday.get("description", "No description available"),
            holiday["country"]["id"],
            holiday["date"]["iso"]
        ))

    conn.commit()
    conn.close()


def main():
    """
    Main function to fetch and store holidays in the database.
    """
    print("Initializing database...")
    initialize_database(DATABASE_NAME)

    print(f"Fetching holidays for {COUNTRY_CODE} in {YEAR}...")
    holidays = fetch_holidays(CALENDAR_API_KEY, COUNTRY_CODE, YEAR)

    if holidays:
        print(f"Fetched {len(holidays)} holidays. Storing in database...")
        store_holidays_in_db(holidays, DATABASE_NAME)
        print("Holiday data stored successfully!")
    else:
        print("No holiday data fetched or an error occurred.")


if __name__ == "__main__":
    main()
