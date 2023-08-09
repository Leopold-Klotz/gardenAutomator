import sqlite3
import asyncio

async def setup_db():
    # Connect to the database or create it if it doesn't exist
    conn = sqlite3.connect('environment.db')
    cursor = conn.cursor()

    # Create the 'measurement_data' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurement_data (
            id INTEGER PRIMARY KEY,
            temperature float NOT NULL,
            humidity float NOT NULL
        )
    ''')

    # Create the 'average_data' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            temperature float NOT NULL,
            humidity float NOT NULL,
            lights boolean NOT NULL,
            fan boolean NOT NULL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

async def store_minute_data(measurements):
    # Connect to the database
    conn = sqlite3.connect('environment.db')
    cursor = conn.cursor()

    # Insert the measurements into the 'measurement_data' table
    cursor.execute('''
        INSERT INTO measurement_data (temperature, humidity)
        VALUES (?, ?)
    ''', measurements)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

async def store_minute_data(lights, fan):
    # Connect to the database
    conn = sqlite3.connect('environment.db')
    cursor = conn.cursor()

    # if length of measurement_data is greater than or equal to 60 average and store in average_data
    cursor.execute('''
        SELECT COUNT(*)
        FROM measurement_data
    ''')

    # Fetch the result
    count = cursor.fetchone()

    if count >= 60:
        # Calculate the average temperature and humidity during the provided hours
        cursor.execute('''
            SELECT AVG(temperature), AVG(humidity)
            FROM measurement_data
        ''')

        # Fetch the result
        avg_temp, avg_humidity = cursor.fetchone()

        # Insert the measurements into the 'measurement_data' table
        cursor.execute('''
            INSERT INTO entries (temperature, humidity, lights, fan)
            VALUES (?, ?, ?, ?)
        ''', (avg_temp, avg_humidity, lights, fan))

        # Delete the entries from the 'measurement_data' table
        cursor.execute('''
            DELETE FROM measurement_data
        ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

async def fetch_avg_data():
    # Connect to the database
    conn = sqlite3.connect('environment.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM average_data
    ''')
    
    # Fetch all the results
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

async def delete_avg_data():
    # Connect to the database
    conn = sqlite3.connect('environment.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM average_data
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

