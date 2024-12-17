import sqlite3
import matplotlib.pyplot as plt 
import pandas as pd
import os
import matplotlib.dates as mdates

def main():
    database_path = os.path.join(os.path.dirname(__file__), "database.db")

    conn = sqlite3.connect(database_path)

    query = """
    SELECT 
        d.date, 
        taq.avg_temp_f, 
        taq.avg_ozone_ppm
    FROM 
        temp_and_airquality AS taq
    JOIN 
        dates AS d
    ON 
        d.id = taq.date
    WHERE 
        d.date BETWEEN '2024-09-01' AND '2024-12-09';
    """

    #load data into pandas dataframe
    df = pd.read_sql_query(query, conn)

    #convert date column to datetime for better readability
    df['date'] = pd.to_datetime(df['date'])

    conn.close()

    #double axis plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    #y-axis: avg temp 
    ax1.plot(df['date'], df['avg_temp_f'], color='tab:red', label='Temperature (°F)', marker='o')
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Temperature (°F)', color='tab:red', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True, which='both', linestyle='--', alpha=0.5)

    #y-axis: ozone levels
    ax2 = ax1.twinx()
    ax2.plot(df['date'], df['avg_ozone_ppm'], color='tab:blue', label='Ozone Level (ppm)', marker='x')
    ax2.set_ylabel('Ozone Level (ppm)', color='tab:blue', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    #format for readability
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  #ticks every week
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  #format as month, day
    plt.xticks(rotation=45, ha='right') 

    plt.title('Average Temperature and Ozone Levels in Ann Arbor from September to December', fontsize=14)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.show()