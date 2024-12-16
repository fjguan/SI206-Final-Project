import sqlite3
import os
import csv

database_path = os.path.join(os.path.dirname(__file__), "full_database.db")
conn = sqlite3.connect(database_path)
curr = conn.cursor()

def weekly_averages():
  file = "weekly_averages.txt"

  curr.execute(
    """
    SELECT aq.date, aq.average, w.avg_temp FROM air_quality AS aq
    JOIN Weather AS w ON aq.date = w.date
    """
  )

  data = curr.fetchall()
  
  prev = 0
  with open(file, "w") as csvfile:
    headers = ["week", "avg_temp", "avg_ozone", "holiday_count"]
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for i in range(7, len(data), 7):
      aq_avg = 0
      aq_total = 0
      temp_avg = 0
      temp_total = 0

      for entry in data[prev:i]:
        aq_total += entry[1]
        temp_total += entry[2]

      aq_avg = aq_total / (i - prev)
      temp_avg = temp_total / (i - prev)

      curr.execute(
        """
        SELECT COUNT(*) AS holiday_count FROM holidays
        WHERE date BETWEEN ? AND ?
        """,
        (data[prev][0], data[i][0])
      )

      holiday_count = curr.fetchone()
      writer.writerow([data[prev][0], round(temp_avg, 2), round(aq_avg, 4), holiday_count[0]])
      # file.write(f"WEEK OF {data[prev][0]}\n")
      # file.write(f"Average Temperature (°F): {round(temp_avg, 2)}\n")
      # file.write(f"Average Ozone Level (ppm): {round(aq_avg, 4)}\n")
      # file.write(f"Holiday Count: {holiday_count[0]}\n\n")

      prev = i


def main():
  weekly_averages()


if __name__ == "__main__":
  main()