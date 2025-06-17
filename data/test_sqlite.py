import sqlite3

# Connect to the database
conn = sqlite3.connect("../data/customer_data.db")
cursor = conn.cursor()

# Query the rfm table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Close the connection
conn.close()
