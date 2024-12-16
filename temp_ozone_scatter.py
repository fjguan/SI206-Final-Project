import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

database_path = os.path.join(os.path.dirname(__file__), "full_database.db")
conn = sqlite3.connect(database_path)
curr = conn.cursor()

def graph():
  aqs = []
  temps = []

  curr.execute(
    """
    SELECT aq.average, w.avg_temp FROM air_quality AS aq
    JOIN Weather AS w ON aq.date = w.date
    """
  )

  data = curr.fetchall()
  for entry in data:
    aqs.append(round(entry[0], 4))
    temps.append(entry[1])

  plt.scatter(temps, aqs)
  plt.xlabel("Temperature (°F)")
  plt.ylabel("Ozone Level (ppm)")
  plt.title("Scatterplot of Temperature vs Ozone Level")
  b, a = np.polyfit(temps, aqs, deg = 1)
  xseq = np.linspace(20, 80)
  plt.plot(xseq, a + b * xseq, color = "tab:red", lw = 2.5)

  plt.show()


def main():
  graph()


if __name__ == "__main__":
  main()