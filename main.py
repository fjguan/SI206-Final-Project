"""
FINAL PROJECT
Team members: Faye Guan, Jenny Shin, Bryan Holmes
"""

import sqlite3
import requests
import re
import weatherapi
import airquality
import holiday
import temperature_ozone_visualization
import holidayvisual
import temp_ozone_vis
import temp_ozone_scatter
import calculations

db = "full_database.db"
conn = sqlite3.connect(db)
curr = conn.cursor()

def create_db():
  weatherapi.main(db)
  airquality.main(db)
  holiday.main(db)

def visualizations():
  temperature_ozone_visualization.main()
  holidayvisual.main()
  temp_ozone_vis.main()
  temp_ozone_scatter.main()


def calculation():
  calculations.main()


def main():
  option = input("1: Database Setup (run five times)\n2: Visualizations\n3: Calculations\nPlease input number: ")
  if option == "1":
    create_db()
  elif option == "2":
    visualizations()
  elif option == "3":
    calculation()
  else:
    print("Invalid option, terminating...")


if __name__ == "__main__":
  main()