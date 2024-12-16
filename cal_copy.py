import requests
import sqlite3

# API Key and Configuration
CALENDAR_API_KEY = "mEqFBnqUJrid9qOl3seOq8gyYFlPSPyx"
DATABASE_NAME = "holidays.db"
COUNTRY_CODE = "US"  # United States
STATE_CODE = "us-mi"  # Michigan
YEAR = 2024  # Year to fetch holidays for
MONTHS = [9, 10, 11, 12]  # September to December
HOLIDAY_LIMIT = 25  # Total number of rows to store in the database


def fetch_holidays(api_key, country, state, year, month):
    """
    Fetch holiday data for a specific month from the Calendarific API.

    Args:
        api_key (str): API key for Calendarific.
        country (str): Country code (e.g., "US").
        state (str): State code (e.g., "us-mi").
        year (int): Year for which to fetch holidays.
        month (int): Month to fetch holidays for.

    Returns:
        list: A list of holiday dictionaries.
    """
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": api_key,
        "country": country,
        "location": state,
        "year": year,
        "month": month,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("response", {}).get("holidays", [])
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


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
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            country TEXT NOT NULL,
            state TEXT,
            date TEXT NOT NULL, 
            type TEXT
        )
    ''')

    conn.commit()
    conn.close()


def store_holidays_in_db(holidays, db_name, state, total_inserted):
    """
    Store holiday data into the SQLite database.

    Args:
        holidays (list): List of holiday dictionaries.
        db_name (str): Name of the SQLite database file.
        state (str): The state where the holidays are relevant.
        total_inserted (int): The cumulative count of holidays inserted.

    Returns:
        int: The number of holidays inserted in this batch.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    rows_inserted = 0

    for holiday in holidays:
        if total_inserted >= HOLIDAY_LIMIT:
            break  # Stop if the total holiday limit is reached

        try:
            cursor.execute('''
                INSERT INTO holidays (name, description, country, state, date, type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                holiday["name"],
                holiday.get("description", "No description available"),
                holiday["country"]["id"],
                state,
                holiday["date"]["iso"],
                holiday["type"][0]
            ))
            rows_inserted += 1
            total_inserted += 1
        except sqlite3.IntegrityError:
            # Skip duplicate holiday names
            print(f"Duplicate holiday '{holiday['name']}' already exists in the database. Skipping...")

    conn.commit()
    conn.close()
    return rows_inserted, total_inserted


def main():
    """
    Main function to fetch and store holidays in the database.
    """
    print("Initializing database...")
    initialize_database(DATABASE_NAME)

    total_holidays_stored = 0

    # Loop through the months (September to December)
    for month in MONTHS:
        if total_holidays_stored >= HOLIDAY_LIMIT:
            print("Holiday limit reached. Stopping.")
            break  # Stop fetching if we've reached the limit

        print(f"Fetching holidays for {STATE_CODE} in {YEAR}, month: {month}...")
        holidays = fetch_holidays(CALENDAR_API_KEY, COUNTRY_CODE, STATE_CODE, YEAR, month)

        if holidays:
            print(f"Fetched {len(holidays)} holidays for month {month}. Storing in database...")
            rows_inserted, total_holidays_stored = store_holidays_in_db(holidays, DATABASE_NAME, STATE_CODE, total_holidays_stored)
            print(f"Inserted {rows_inserted} holidays. Total stored: {total_holidays_stored}")
        else:
            print(f"No holidays found for month {month} or an error occurred.")

    print(f"Total holidays stored: {total_holidays_stored}")


if __name__ == "__main__":
    main()
