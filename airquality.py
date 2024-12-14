import requests
import sqlite3
import pandas as pd

# country = "us"
# city = "Ann Arbor"
# ID = 8873
KEY = "782b9258e860dc55dd506547926a0ceac5ab9097301988e4eecf4cf36b8ccaf4"
DB = "air_quality.db"
COUNTRY = "us"
CITY = "Ann Arbor"

conn = sqlite3.connect(DB)
curr = conn.cursor()

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

def fetch_data(location_id, start_date, end_date):
  url = f'https://api.openaq.org/v2/averages'
  headers = {"X-API-KEY": KEY}

  start_date = start_date + "T00:00:00+00:00"
  end_date = end_date + "T23:59:00+00:00"
  params = {
    "temporal": "day",
    "locations_id": location_id,
    "date_from": start_date,
    "date_to": end_date,
    "limit": 25
  }

  response = requests.get(url, headers = headers, params = params)
  location_data = response.json()

  return response.json()

  # measurements = [{"date": row["day"], "average": row["average"], "parameter": row["parameter"], "units": row["unit"]} for row in location_data["results"]]
  # df = pd.DataFrame.from_dict(measurements)

  # print(df)

def process_data(start, end):
  id = get_city_id()
  data = fetch_data(id, start, end)
  for entry in data["results"]:
    date = entry["day"].strip()
    print(date)
    average = entry["average"]
    parameter = entry["parameter"]
    units = entry["unit"]
    insert_data(date, average, parameter, units)

  curr.execute(
    """
    SELECT * FROM air_quality
    ORDER BY date(date) ASC
    """
  )

  conn.commit()

def main():
  start = input("Enter a starting date (YYYY-MM-DD): ")
  end = input("Enter an ending date (YYYY-MM-DD): ")
  create_db()
  process_data(start, end)

if __name__ == "__main__":
  main()