import requests 
import sqlite3 

calendar_api_key = "mEqFBnqUJrid9qOl3seOq8gyYFlPSPyx"
database_name = "holidays.db"
country_code = "US"
location = 'Ann Arbor, Michigan'
start_date = '2024-09-01'
end_date = '2024-12-09'
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
    initialize_database(database_name)

    print(f"Fetching holidays for {country_code} in {start_date}...")
    holidays = fetch_holidays(calendar_api_key, country_code, start_date, end_date)

    if holidays:
        print(f"Fetched {len(holidays)} holidays. Storing in database...")
        store_holidays_in_db(holidays, database_name)
        print("Holiday data stored successfully!")
    else:
        print("No holiday data fetched or an error occurred.")


if __name__ == "__main__":
    main()