import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# File paths
DB_PATH = "data/customer_data.db"

def load_rfm_data():
    """Load RFM data from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM rfm", conn)
    conn.close()
    return df

def perform_clustering(df, n_clusters=4):
    """Perform K-means clustering on RFM data."""
    # Prepare features (Recency, Frequency, Monetary)
    features = df[['recency', 'frequency', 'monetary']]
    
    # Scale the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['segment'] = kmeans.fit_predict(scaled_features)
    
    # Map segment numbers to meaningful labels
    segment_labels = {
        0: "Loyal Customers",
        1: "At-Risk Customers",
        2: "New Customers",
        3: "Lost Customers"
    }
    df['segment_label'] = df['segment'].map(segment_labels)
    
    return df

def save_segments(df):
    """Save the segment labels back to SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # Add segment labels to the rfm table
    df[['customer_id', 'recency', 'frequency', 'monetary', 'segment', 'segment_label']].to_sql('rfm', conn, if_exists='replace', index=False)
    conn.close()

def main():
    """Run the clustering pipeline."""
    print("Loading RFM data...")
    rfm_df = load_rfm_data()
    
    print("Performing clustering...")
    clustered_df = perform_clustering(rfm_df)
    
    print("Saving segments to database...")
    save_segments(clustered_df)
    
    print("Clustering completed successfully!")
    print(clustered_df[['customer_id', 'segment_label']].head())

if __name__ == "__main__":
    main()