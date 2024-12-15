import requests
import sqlite3
from datetime import datetime, timedelta

# ID = 8873
KEY = "782b9258e860dc55dd506547926a0ceac5ab9097301988e4eecf4cf36b8ccaf4"
COUNTRY = "us"
CITY = "Ann Arbor"
start_date = "2024-09-01" 
end_date = "2024-12-09"  
limit = 25 

def create_db():
  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS air_quality (
      date TEXT,
      average REAL,
      parameter TEXT,
      units TEXT,
      UNIQUE(date, average, parameter, units)
    )
    """
  )

  conn.commit() 


def insert_data(date, average, parameter, units):
  curr.execute(
    """
    INSERT OR IGNORE INTO air_quality (date, average, parameter, units)
    VALUES (?, ?, ?, ?)
    """,
    (date, average, parameter, units)
  )

  conn.commit()


def get_city_id():
  url = f'https://api.openaq.org/v2/locations?country={COUNTRY}&city={CITY}'
  headers = {"X-API-KEY": KEY}

  city_response = requests.get(url, headers = headers)
  city_data = city_response.json()

  for entry in city_data["results"]:
    if entry["name"] == CITY:
      id = entry["id"]

  return id


def fetch_data(location_id):
  url = f'https://api.openaq.org/v2/averages'
  headers = {"X-API-KEY": KEY}

  curr.execute("SELECT date FROM air_quality")
  existing_dates = {row[0] for row in curr.fetchall()}
  
  date_format = "%Y-%m-%d"
  date = datetime.strptime(start_date, date_format)
  end = datetime.strptime(end_date, date_format)
  new_entries = 0

  while date <= end and new_entries < limit:
    
    if str(date.date()) not in existing_dates:
      start_time = str(date.date()) + "T00:00:00+00:00"
      end_time = str(date.date()) + "T23:59:00+00:00"

      params = {
        "temporal": "day",
        "locations_id": location_id,
        "date_from": start_time,
        "date_to": end_time
      }

      response = requests.get(url, headers = headers, params = params)
      location_data = response.json()

      process_data(location_data)
      new_entries += 1
    
    date += timedelta(days = 1)


def process_data(data):
  for entry in data["results"]:
    date = entry["day"].strip()
    average = entry["average"]
    parameter = entry["parameter"]
    units = entry["unit"]
    insert_data(date, average, parameter, units)


def main(db):
  global conn 
  conn = sqlite3.connect(db)
  global curr 
  curr = conn.cursor()

  create_db()
  id = get_city_id()
  fetch_data(id)

if __name__ == "__main__":
  main()