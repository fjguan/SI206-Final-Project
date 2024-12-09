import requests
import sqlite3
from datetime import datetime, timedelta

weather_api_key = '2ce6143e9a79140595e6e926bcb0a044'

location = 'Detroit, Michigan'
#example dates
start_date = '2023-09-01'  
end_date = '2023-12-10'   
limit = 25 

db_name = "weather_data.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date INTEGER,
    avg_temp INTEGER,
    uv_index INTEGER
)
""")
conn.commit()

cursor.execute("SELECT date FROM Weather")
stored_dates = {row[0] for row in cursor.fetchall()}

url = f"http://api.weatherstack.com/historical?access_key={weather_api_key}&query={location}&units=f"

date_format = "%Y-%m-%d"
current_date = datetime.strptime(start_date, date_format)
end_date_obj = datetime.strptime(end_date, date_format)

new_entries = 0

while current_date <= end_date_obj and new_entries < limit:
    date_str = current_date.strftime(date_format)

    if date_str not in stored_dates:
    
        response = requests.get(f"{url}&historical_date={date_str}")
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                print(f"Error on {date_str}: {data['error']['info']}")
            else:
                historical_data = data.get("historical", {}).get(date_str, {})
                
                if historical_data:
                    avg_temp = historical_data.get("avgtemp", None)
                    uv_index = historical_data.get("uv_index", None)
                else:
                    avg_temp = None
                    uv_index = None
                
                #insert into database
                cursor.execute("""
                INSERT OR IGNORE INTO Weather (date, avg_temp, uv_index)
                VALUES (?, ?, ?)
                """, (date_str, avg_temp, uv_index))
                conn.commit()
                
                new_entries += 1
                print(f"Stored data for {date_str}: Avg Temp={avg_temp}, UV Index={uv_index}")
        
        else:
            print(f"Skipping {date_str} (already in database)")

    #move to the next date
    current_date += timedelta(days=1)

conn.close()
print(f"{new_entries} new entries added to the database.")