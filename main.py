"""
FINAL PROJECT
Team members: Faye Guan, Jenny Shin, Bryan Holmes
"""

import sqlite3
import requests
import matplotlib as plt
import weather_copy
import airqual_copy

def create_db():
  db = "full_database.db"
  conn = sqlite3.connect(db)
  curr = conn.cursor()
  weather_copy.main(db)
  airqual_copy.main(db)


def main():
  create_db()

if __name__ == "__main__":
  main()