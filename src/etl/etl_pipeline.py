import pandas as pd
import sqlite3
from datetime import datetime
import os

# File paths
DATA_RAW_PATH = "data/raw/Online_Retail.xlsx"  # Adjust if using Online Retail.xlsx
DB_PATH = "data/customer_data.db"

def extract_data():
    """Extract data from the raw CSV file."""
    # Check if the file exists
    if not os.path.exists(DATA_RAW_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_RAW_PATH}. Please place the UCI Online Retail dataset in data/raw/.")
    
    # Read the CSV file
    df = pd.read_excel(DATA_RAW_PATH, engine='openpyxl')
    return df

def transform_data(df):
    """Transform the data to calculate RFM metrics."""
    # Data cleaning
    df = df.dropna(subset=['CustomerID'])  # Remove rows with missing CustomerID
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    # Define the reference date (use the latest date in the dataset + 1 day)
    reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    # Calculate RFM metrics
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,  # Recency
        'InvoiceNo': 'nunique',  # Frequency
        'TotalPrice': 'sum'  # Monetary
    }).reset_index()
    
    # Rename columns
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    return rfm

def load_data(rfm_df):
    """Load the RFM data into the SQLite database."""
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert data into the rfm table
    rfm_df.to_sql('rfm', conn, if_exists='replace', index=False)
    
    # Commit and close
    conn.commit()
    conn.close()

def main():
    """Run the ETL pipeline."""
    print("Starting ETL pipeline...")
    
    # Extract
    print("Extracting data...")
    df = extract_data()
    
    # Transform
    print("Transforming data...")
    rfm_df = transform_data(df)
    
    # Load
    print("Loading data into SQLite...")
    load_data(rfm_df)
    
    print("ETL pipeline completed successfully!")
    print(f"RFM metrics for {len(rfm_df)} customers have been loaded into the database.")

if __name__ == "__main__":
    main()