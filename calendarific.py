import requests 
import sqlite3 

calendar_api_key = "mEqFBnqUJrid9qOl3seOq8gyYFlPSPyx"

# Function to fetch holiday data from Calendarific API
def fetch_holidays(api_key, country, year):
    base_url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": api_key,
        "country": country,
        "year": year,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()["response"]["holidays"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# Function to store holiday data into SQLite database
def store_holidays_in_db(holidays, db_name="holidays.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            country TEXT,
            date TEXT
        )
    ''')

    # Insert holiday data into table
    for holiday in holidays:
        cursor.execute('''
            INSERT INTO holidays (name, description, country, date)
            VALUES (?, ?, ?, ?)
        ''', (
            holiday["name"],
            holiday.get("description", "No description available"),
            holiday["country"]['id'],
            holiday["date"]["iso"]
        ))

    conn.commit()
    conn.close()

# Main script to fetch and store holiday data
def main():
    country = "US"  # Replace with desired country code
    year = 2024      # Replace with desired year

    print("Fetching holiday data...")
    holidays = fetch_holidays(calendar_api_key, country, year)

    if holidays:
        print(f"Fetched {len(holidays)} holidays. Storing in database...")
        store_holidays_in_db(holidays)
        print("Holiday data stored successfully!")
    else:
        print("No holidays fetched or an error occurred.")

if __name__ == "__main__":
    main()

