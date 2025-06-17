import pandas as pd
import sqlite3

# File paths
DB_PATH = "data/customer_data.db"
CSV_PATH = "data/processed/customer_segments_clv.csv"

def export_data():
    """Export RFM, segments, and CLV predictions to CSV."""
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    
    # Load the rfm table
    df = pd.read_sql_query("SELECT * FROM rfm", conn)
    conn.close()
    
    # Export to CSV
    df.to_csv(CSV_PATH, index=False)
    print(f"Data exported successfully to {CSV_PATH}")

if __name__ == "__main__":
    export_data()