import sqlite3
import matplotlib.pyplot as plt
import re
import os

def plot_data(x, y1, y2, ax1, month):

  color1 = "tab:blue"
  color2 = "tab:red"

  ax1.set_title(f"{month}")
  ax1.set_xlabel("Day")
  ax1.set_ylabel("Temperature (°F))", color = color1)
  ax1.plot(x, y1, color = color1)
  ax1.scatter(x, y1, s = 10, color = color1)
  ax1.tick_params(axis = "y", labelcolor = color1)
  ax1.tick_params(axis = "x", labelsize = 7)

  ax2 = ax1.twinx()
  ax2.set_ylabel("Ozone Level (ppm)", color = color2)
  ax2.plot(x, y2, color = color2)
  ax2.scatter(x, y2, s = 10, color = color2)
  ax2.tick_params(axis = "y", labelcolor = color2)


def graph_setup():
  dates = []
  aqs = []
  temps = []

  curr.execute(
    """
    SELECT aq.date, aq.average, w.avg_temp FROM air_quality AS aq
    JOIN Weather AS w ON aq.date = w.date
    """
  )

  data = curr.fetchall()
  pattern = r"(?<=\d{4}-\d{2}-)(\d{2})"
  for entry in data:
    dates.append(re.findall(pattern, entry[0])[0])
    aqs.append(round(entry[1], 4))
    temps.append(entry[2])
  
  fig, axs = plt.subplots(2, 2, figsize = (12, 6))
  
  sept_days = dates[:30]
  sept_temps = temps[:30]
  sept_aqs = aqs[:30]
  plot_data(sept_days, sept_temps, sept_aqs, axs[0, 0], "September")


  oct_days = dates[30:61]
  oct_temps = temps[30:61]
  oct_aqs = aqs[30:61]
  plot_data(oct_days, oct_temps, oct_aqs, axs[0, 1], "October")

  nov_days = dates[61:91]
  nov_temps = temps[61:91]
  nov_aqs = aqs[61:91]
  plot_data(nov_days, nov_temps, nov_aqs, axs[1, 0], "November")

  dec_days = dates[91:]
  dec_temps = temps[91:]
  dec_aqs = aqs[91:]
  plot_data(dec_days, dec_temps, dec_aqs, axs[1, 1], "December")

  fig.suptitle("Line Plots of Temperature and Ozone Levels for Sept 01 - Dec 09")
  fig.tight_layout()
  plt.show()


def main():
  database_path = os.path.join(os.path.dirname(__file__), "full_database.db")
  global conn 
  conn = sqlite3.connect(database_path)
  global curr 
  curr = conn.cursor()

  graph_setup()


if __name__ == "__main__":
  main()