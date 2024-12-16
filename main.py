"""
FINAL PROJECT
Team members: Faye Guan, Jenny Shin, Bryan Holmes
"""

import sqlite3
import requests
import matplotlib as plt
import weatherapi
import airquality
# import cal

db = "full_database.db"
conn = sqlite3.connect(db)
curr = conn.cursor()

def create_db():
  db = "full_database.db"
  weatherapi.main(db)
  airquality.main(db)
  # cal.main(db)


def calculations(start_date, end_date):
  file = "calculations.txt"
  aq_avg = 0
  aq_total = 0
  temp_avg = 0
  temp_total = 0

  curr.execute(
    """
    SELECT average, avg_temp FROM air_quality
    JOIN Weather ON air_quality.date = Weather.date
    WHERE air_quality.date BETWEEN ? AND ?
    """,
    (start_date, end_date)
  )

  data = curr.fetchall()

  for entry in data:
    aq_total += entry[0]
    temp_total += entry[1]
  
  aq_avg = aq_total / len(data)
  temp_avg = temp_total / len(data)

  with open(file, "w") as file:
    file.write(f"FROM {start_date} TO {end_date}\n")
    file.write(f"Average Temperature (F): {temp_avg}\nAverage Ozone Level (ppm): {aq_avg}\n\n")
  
  print(f"Averages for {start_date} to {end_date} added.")


def main():
  option = input("Enter 1 for database setup; enter 2 for calculations and visualizations: ")
  if option == "1":
    create_db()
  elif option == "2":
    calculations("2024-11-24", "2024-11-30")
  else:
    print("Invalid option, terminating...")

if __name__ == "__main__":
  main()