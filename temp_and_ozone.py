import requests
import sqlite3
from datetime import datetime, timedelta

# ID = 8873
AQ_KEY = "782b9258e860dc55dd506547926a0ceac5ab9097301988e4eecf4cf36b8ccaf4"
weather_api_key = '2ce6143e9a79140595e6e926bcb0a044'
COUNTRY = "us"
CITY = "Ann Arbor"
start_date = "2024-09-01" 
end_date = "2024-12-09"  
limit = 25 
location = "Ann Arbor, Michigan"

def create_table():
  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS dates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE
    )
    """
  )

  curr.execute(
    """
    CREATE TABLE IF NOT EXISTS temp_and_airquality (
      date INTEGER,
      avg_temp_f INTEGER,
      uv_index INTEGER,
      avg_ozone_ppm REAL,
      FOREIGN KEY (date) REFERENCES dates(id),
      UNIQUE(avg_temp_f, uv_index, avg_ozone_ppm)
    )
    """
  )

  conn.commit() 


def insert_data(date_id, avg_temp, uv_index, avg_ozone):
  curr.execute(
    """
    INSERT OR IGNORE INTO temp_and_airquality (date, avg_temp_f, uv_index, avg_ozone_ppm)
    VALUES (?, ?, ?, ?)
    """,
    (date_id, avg_temp, uv_index, avg_ozone)
  )

  conn.commit()


def get_city_id():
  url = f'https://api.openaq.org/v2/locations?country={COUNTRY}&city={CITY}'
  headers = {"X-API-KEY": AQ_KEY}

  city_response = requests.get(url, headers = headers)
  city_data = city_response.json()

  for entry in city_data["results"]:
    if entry["name"] == CITY:
      id = entry["id"]

  return id


def fetch_data(location_id):
  aq_url = f'https://api.openaq.org/v2/averages'
  w_url = f"http://api.weatherstack.com/historical?access_key={weather_api_key}&query={location}&units=f"
  headers = {"X-API-KEY": AQ_KEY}

  curr.execute("SELECT date FROM dates")
  existing_dates = {row[0] for row in curr.fetchall()}
  
  date_format = "%Y-%m-%d"
  date = datetime.strptime(start_date, date_format)
  end = datetime.strptime(end_date, date_format)
  new_entries = 0

  print("Storing temperature and ozone data...")
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

      aq_response = requests.get(aq_url, headers = headers, params = params)
      aq_data = aq_response.json()

      w_response = requests.get(f"{w_url}&historical_date={date.strftime(date_format)}")
      w_data = w_response.json()

      process_data(aq_data, w_data, str(date.date()))
      new_entries += 1
    
    date += timedelta(days = 1)
  
  print(f"{new_entries} new entries added to the database.")


def process_data(aq, weather, date):
  for entry in aq["results"]:
    avg_aq = entry["average"]

  historical_data = weather.get("historical", {}).get(date, {})
  avg_temp = historical_data.get("avgtemp", None)
  uv_index = historical_data.get("uv_index", None)
  
  curr.execute(
    """
    INSERT OR IGNORE INTO dates (date)
    VALUES (?)
    """,
    (date,)
  )

  curr.execute(
    """
    SELECT id FROM dates WHERE date = ?
    """,
    (date,)
  )

  date_id = curr.fetchone()[0]
  insert_data(date_id, avg_temp, uv_index, avg_aq)



def main(db):
  global conn 
  conn = sqlite3.connect(db)
  global curr 
  curr = conn.cursor()

  create_table()
  id = get_city_id()
  fetch_data(id)

if __name__ == "__main__":
  main()