import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# File paths
DB_PATH = "data/customer_data.db"

def load_data():
    """Load RFM and segment data from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM rfm", conn)
    conn.close()
    return df

def train_clv_model(df):
    """Train an XGBoost model to predict CLV."""
    # Features: recency, frequency, and segment (encoded)
    X = df[['recency', 'frequency', 'segment']]
    # Target: monetary (as a proxy for CLV)
    y = df['monetary']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    model.fit(X_train, y_train)
    
    # Predict on the entire dataset
    df['clv_predicted'] = model.predict(X)
    
    # Evaluate the model on the test set
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error on test set: {mse:.2f}")
    
    return df

def save_clv_predictions(df):
    """Save the CLV predictions to SQLite."""
    conn = sqlite3.connect(DB_PATH)
    df[['customer_id', 'recency', 'frequency', 'monetary', 'segment', 'segment_label', 'clv_predicted']].to_sql('rfm', conn, if_exists='replace', index=False)
    conn.close()

def main():
    """Run the CLV prediction pipeline."""
    print("Loading data...")
    df = load_data()
    
    print("Training CLV model...")
    df = train_clv_model(df)
    
    print("Saving CLV predictions...")
    save_clv_predictions(df)
    
    print("CLV prediction completed successfully!")
    print(df[['customer_id', 'clv_predicted']].head())

if __name__ == "__main__":
    main()