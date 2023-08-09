import sqlite3

# connect to the sqlite database
connection = sqlite3.connect('data.db')

# create a cursor
cursor = connection.cursor()

# create table
cursor.execute("""
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    humidity REAL,
    lights BOOLEAN,
    fan BOOLEAN
)
""")

# commit the changes and close the connection
connection.commit()
connection.close()
