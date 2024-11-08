
import sqlite3
import csv

# Function to load apparel data from a CSV file
def load_apparel_data_from_csv(csv_file):
    apparel_data = []
    
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            apparel_data.append((row[0], row[1], row[2]))  # Append the apparel_id, name, and image_path
    
    return apparel_data

# Connect to SQLite database
conn = sqlite3.connect('apparel.db')
cursor = conn.cursor()

# Load apparel data from CSV
csv_file = 'apparel_data.csv'
apparel_data = load_apparel_data_from_csv(csv_file)

# Insert apparel data into the database
cursor.executemany('''
INSERT OR REPLACE INTO apparel (apparel_id, name, image_path) VALUES (?, ?, ?)
''', apparel_data)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Apparel data inserted successfully from CSV.")
