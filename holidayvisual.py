import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import os

# Database Path (absolute path to ensure correctness)
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "full_database.db")

# Test database connection (using the holidays.database)
# if not os.path.exists(DATABASE_PATH):
#     raise FileNotFoundError(f"Error: Database file not found at {DATABASE_PATH}")
# else:
#     print(f"Using database at {DATABASE_PATH}")

def load_holiday_data(db_path):
    """
    Load and merge holidays and holiday_types tables into a single DataFrame.
    """
    conn = sqlite3.connect(db_path)
    query = '''
        SELECT ht.type_name, COUNT(h.id) AS holiday_count
        FROM holidays h
        JOIN holiday_types ht ON h.holiday_type_id = ht.id
        GROUP BY ht.type_name;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_holidays_per_type(df): #drawing for the holiday visualization
    """
    Plot a bar graph showing the number of holidays per holiday type.
    """
    # x different holiday types 
    # y number of holidays 
    plt.figure(figsize=(10, 6))
    plt.bar(df['type_name'], df['holiday_count'], color="tab:blue")
    plt.title("Number of Holidays per Holiday Type", fontsize=16)
    plt.xlabel("Holiday Type", fontsize=14)
    plt.ylabel("Number of Holidays", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def main(): 
    # Load data from the database
    holidays_df = load_holiday_data(DATABASE_PATH)

    # Plot the bar graph
    plot_holidays_per_type(holidays_df)

# # Main script execution
if __name__ == "__main__":
    main()