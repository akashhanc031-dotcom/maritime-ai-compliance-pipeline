import sqlite3
import csv

# 1. Connect to (or create) the database file
conn = sqlite3.connect('maritime_fleet.db')
cursor = conn.cursor()

# 2. Create the 'ships' table with proper data types
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_name TEXT,
        tonnage INTEGER,
        fuel_consumed REAL
    )
''')

# 3. Load data from your CSV into the SQL Table
try:
    with open('fleet_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT INTO ships (ship_name, tonnage, fuel_consumed)
                VALUES (?, ?, ?)
            ''', (row['ship_name'], row['tonnage'], row['fuel_consumed']))
    
    conn.commit()
    print("✅ SQL Database 'maritime_fleet.db' created and data loaded successfully!")
except FileNotFoundError:
    print("❌ Error: 'fleet_data.csv' not found. Make sure it is in the same folder.")
finally:
    conn.close()