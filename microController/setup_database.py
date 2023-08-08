import sqlite3
import asyncio

async def create_db():
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