import requests
import sqlite3
import re

# API Key and Configuration
CALENDAR_API_KEY = "mEqFBnqUJrid9qOl3seOq8gyYFlPSPyx"
# DATABASE_NAME = "holidays.db"
COUNTRY_CODE = "US"  
STATE_CODE = "us-mi"  # Michigan
YEAR = 2024  # Year 
MONTHS = [9, 10, 11, 12]  # September to December
HOLIDAY_LIMIT = 25  # rows


def fetch_holidays(api_key, country, state, year, month):
    """
    Fetch holiday data for a specific month from the Calendarific API.
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
    Create or initialize the SQLite database with two tables:
    1. holidays
    2. holiday_types
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # create the table 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holiday_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT UNIQUE NOT NULL
        )
    ''')

    # table for foreign key reference to holiday_types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            holiday_type_id INTEGER NOT NULL,
            country TEXT NOT NULL,
            state TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (holiday_type_id) REFERENCES holiday_types(id)
        )
    ''')

    conn.commit()
    conn.close()


def store_holidays_in_db(holidays, db_name, state, count):
    """
    Store holiday data into the SQLite database, including holiday types.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # rows_inserted = 0

    for holiday in holidays:
        # holiday type insert into holiday_type (not exists)
        holiday_type = holiday.get("type", [])
        holiday_type_name = holiday_type[0] if isinstance(holiday_type, list) and holiday_type else "Unknown"
        
        #  already exists
        cursor.execute('''
            INSERT OR IGNORE INTO holiday_types (type_name)
            VALUES (?)
        ''', (holiday_type_name,))

        # Fetch the holiday_type_id for the holiday
        cursor.execute('''
            SELECT id FROM holiday_types WHERE type_name = ?
        ''', (holiday_type_name,))
        holiday_type_id = cursor.fetchone()[0]

        # Insert holiday into the holidays table
        try:
            pattern = r"^\d{4}-\d{2}-\d{2}"
            cursor.execute('''
                INSERT INTO holidays (name, holiday_type_id, country, state, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                holiday["name"],
                holiday_type_id,
                holiday["country"]["id"],
                state,
                re.findall(pattern, holiday["date"]["iso"])[0]
            ))
            count += 1
            # total limit 
            if count >= HOLIDAY_LIMIT:
                break
        except sqlite3.IntegrityError:
            # no duplicate 
            # print(f"Duplicate holiday '{holiday['name']}' already exists in the database. Skipping...")
            pass

    conn.commit()
    conn.close()
    return count


def main(db):
    """
    Main function to fetch and store holidays in the database.
    """
    print("Initializing database...")
    initialize_database(db)

    total_holidays_stored = 0
    count = 0

    # (September to December)
    for month in MONTHS:
        # if total_holidays_stored >= HOLIDAY_LIMIT:
        #     break  # stop for limit 25 
        print(f"Fetching holidays for {STATE_CODE} in {YEAR}, month: {month}...")
        holidays = fetch_holidays(CALENDAR_API_KEY, COUNTRY_CODE, STATE_CODE, YEAR, month)

        if holidays:
            # print(f"Fetched {len(holidays)} holidays for month {month}. Storing in database...")
            count = store_holidays_in_db(holidays, db, STATE_CODE, count)
            total_holidays_stored += count

        if total_holidays_stored >= HOLIDAY_LIMIT:
            print(f"Holiday limit reached: {HOLIDAY_LIMIT}. Stopping insertion.")
            break
        # else:
        #     print(f"No holidays found for month {month} or an error occurred.")

    print(f"Total holidays stored: {total_holidays_stored}")


if __name__ == "__main__":
    main()
