import sqlite3

# Function creates the database and tables
def setup_db():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

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

    cursor.execute("""
    CREATE TABLE relay_state (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        lights BOOLEAN,
        fan BOOLEAN
    )   
    """)

    connection.commit()
    connection.close()

# Function stores the up-to-date data in the database
def store_data(data):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO sensor_data (timestamp, temperature, humidity, lights, fan)
    VALUES (datetime('now'), ?, ?, ?, ?)
    """, (data['Temperature'], data['Humidity'], data['Lights'], data['Fan']))

    connection.commit()
    connection.close()

    # return a confirmation message
    return {"message": "Data stored"}

# Function updates the relays
def update_relays(data):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO relay_state (timestamp, lights, fan)
    VALUES (datetime('now'), ?, ?)
    """, (data['Lights'], data['Fan']))

    # change most recent data in sensor_data
    cursor.execute("""
    UPDATE sensor_data
    SET lights = ?, fan = ?
    WHERE id = (SELECT MAX(id) FROM sensor_data)
    """, (data['Lights'], data['Fan']))

    connection.commit()
    connection.close()

    # return a confirmation message
    return {"message": "Relays updated"}

# Function returns the average temperature and humidity during the provided hours
def calculate_average(hours):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""
    SELECT AVG(temperature), AVG(humidity)
    FROM sensor_data
    WHERE timestamp > datetime('now', '-{} hours')
    """.format(hours)) 

    avg_temp, avg_humidity = cursor.fetchone()
    connection.close()
    return {'Average Temperature': avg_temp, 'Average Humidity': avg_humidity}

# Function returns the data over the provided hours
def fetch_history(hours):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""
    SELECT timestamp, temperature, humidity, lights, fan
    FROM sensor_data
    WHERE timestamp > datetime('now', '-{} hours')
    """.format(hours))

    rows = cursor.fetchall()
    connection.close()
    return rows

# Function deletes the data over the provided hours
def delete_history(hours):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM sensor_data
    WHERE timestamp > datetime('now', '-{} hours')
    """.format(hours))

    connection.commit()
    connection.close()
    return {"message": "Data deleted"}

# Function returns the most recent data
def display_update():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""
    SELECT timestamp, temperature, humidity, lights, fan
    FROM sensor_data
    ORDER BY timestamp DESC
    LIMIT 1
    """)

    rows = cursor.fetchall()
    connection.close()
    message = {"Temperature": rows[0][1], "Humidity": rows[0][2], "Lights": rows[0][3], "Fan": rows[0][4]}
    return message

if __name__ == "__main__":
    setup_db()