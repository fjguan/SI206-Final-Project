import requests
import sqlite3
from datetime import datetime

# Constants
calendar_api_key = "mEqFBnqUJrid9qOl3seOq8gyYFlPSPyx"
database_name = "holidays.db"
country_code = "US"

start_date = "2024-09-01"
end_date = "2024-12-09"


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

def store_holidays_in_db(holidays, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for holiday in holidays:
        print(f"Inserting into DB: {holiday['name']} on {holiday['date']['iso']}")
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