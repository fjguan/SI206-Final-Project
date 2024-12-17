"""
FINAL PROJECT
Team members: Faye Guan, Jenny Shin, Bryan Holmes
"""

import sqlite3
import temp_and_ozone
import holiday
import temperature_ozone_visualization
import holidayvisual
import temp_ozone_vis
import temp_ozone_scatter
import ozone_holiday_vis
import calculations

db = "database.db"
conn = sqlite3.connect(db)
curr = conn.cursor()

def create_db():
  temp_and_ozone.main(db)
  holiday.main(db)

def visualizations():
  temperature_ozone_visualization.main()
  holidayvisual.main()
  temp_ozone_vis.main()
  temp_ozone_scatter.main()
  # ozone_holiday_vis.main()


def calculation():
  calculations.main()


def main():
  option = input("1: Database Setup (run six times)\n2: Visualizations\n3: Calculations\nPlease input number: ")
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