import sqlite3
import matplotlib.pyplot as plt 
import pandas as pd
import os


def main():
    database_path = os.path.join(os.path.dirname(__file__), "full_database.db")

    conn = sqlite3.connect(database_path)

    query = """
    SELECT 
        holidays.name, 
        air_quality.average, 
        holidays.date 
    FROM 
        holidays
    JOIN 
        air_quality 
    ON 
        holidays.date = air_quality.date
    WHERE 
        holidays.name IN ('Thanksgiving Day', 'Day After Thanksgiving', 'Halloween', 
        'Labor Day', 'Election Day', 'Black Friday', 'Friday the 13th',
        'World Tourism Day');
    """

    df = pd.read_sql_query(query, conn)

    df['date'] = pd.to_datetime(df['date'])
    conn.close()

    plt.figure(figsize=(10, 6))
    plt.bar(df['name'], df['average'], color='skyblue', edgecolor='black')

    plt.xlabel('Holiday', fontsize=12)
    plt.ylabel('Ozone Level (ppb)', fontsize=12)
    plt.title('Ozone Levels on Holidays', fontsize=14)

    plt.xticks(rotation=45, ha='right')

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

if __name__ == "__main__":
    main()