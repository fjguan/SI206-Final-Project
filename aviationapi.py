import requests
import sqlite3

KEY = "b380d61cb23d88708e7e528a552f28fa"
URL = "http://api.aviationstack.com/v1/flights"
DB = "aviation_data.db"


conn = sqlite3.connect(DB)
curr = conn.cursor()

def create_db():
  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS departures (
      flight_date TEXT,
      flight_status TEXT,
      delay INTEGER,
      UNIQUE(flight_date, flight_status, delay)
    )
    """
  )

  conn.commit()

def insert_data(flight_date, flight_status, delay):
  curr.execute(
    """
    INSERT OR IGNORE INTO departures (flight_date, flight_status, delay)
    VALUES (?, ?, ?)
    """,
    (flight_date, flight_status, delay)
  )

  conn.commit()

def fetch_data():
  params = {
    "access_key": KEY,
    "dep_iata": "DTW", 
    #"flight_date": "2024-09-01",
    "limit": 25
  }

  response = requests.get(URL, params = params)
  data = response.json()

  return data

def process_data():
  data = fetch_data()
  print(data)
  count = 0
  for flight in data['data']:
    flight_date = flight["flight_date"]
    flight_status = flight["flight_status"]
    delay = flight["departure"]["delay"]
    insert_data(flight_date, flight_status, delay)

if __name__ == "__main__":
  create_db()
  process_data()