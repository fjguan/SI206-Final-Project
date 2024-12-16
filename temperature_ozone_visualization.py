import sqlite3
import matplotlib.pyplot as plt 
import pandas as pd
import os
import matplotlib.dates as mdates


database_path = os.path.join(os.path.dirname(__file__), "full_database.db")


# Connect to the SQLite database
conn = sqlite3.connect(database_path)

# Define the SQL query
query = """
SELECT 
    Weather.date, 
    Weather.avg_temp, 
    air_quality.average
FROM 
    Weather
JOIN 
    air_quality
ON 
    Weather.date = air_quality.date
WHERE 
    Weather.date BETWEEN '2024-09-01' AND '2024-12-09';
"""


# Execute the query and load the data into a pandas DataFrame
df = pd.read_sql_query(query, conn)

df['date'] = pd.to_datetime(df['date'])
# Close the connection
conn.close()

# Check the DataFrame (optional)
print(df)

# Create the dual-axis plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Primary y-axis: Temperature
ax1.plot(df['date'], df['avg_temp'], color='tab:red', label='Temperature (°F)', marker='o')
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Temperature (°F)', color='tab:red', fontsize=12)
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, which='both', linestyle='--', alpha=0.5)

# Secondary y-axis: Ozone Levels
ax2 = ax1.twinx()
ax2.plot(df['date'], df['average'], color='tab:blue', label='Ozone Level (ppb)', marker='x')
ax2.set_ylabel('Ozone Level (ppb)', color='tab:blue', fontsize=12)
ax2.tick_params(axis='y', labelcolor='tab:blue')

#format for readability
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # Place ticks every week
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Format ticks as "Month Day"
plt.xticks(rotation=45, ha='right') 
# Title and Legend
plt.title('Average Temperature and Ozone Levels in Ann Arbor', fontsize=14)


# Add legends for both axes
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show the plot
plt.show()