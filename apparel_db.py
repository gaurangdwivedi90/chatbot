import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('apparel.db')
cursor = conn.cursor()

# Create a table to store apparel data, including image paths
cursor.execute('''
CREATE TABLE IF NOT EXISTS apparel (
    apparel_id TEXT PRIMARY KEY,
    name TEXT,
    image_path TEXT
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")