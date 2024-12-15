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

def create_db():
  db = "full_database.db"
  conn = sqlite3.connect(db)
  curr = conn.cursor()
  weatherapi.main(db)
  airquality.main(db)
  # cal.main(db)


def main():
  create_db()

if __name__ == "__main__":
  main()