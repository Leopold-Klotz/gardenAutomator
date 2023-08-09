import sqlite3

def setup_db():
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

def store_data(data):
    # connect to the sqlite database
    connection = sqlite3.connect('data.db')

    # create a cursor
    cursor = connection.cursor()

    # insert data into table
    cursor.execute("""
    INSERT INTO sensor_data (timestamp, temperature, humidity, lights, fan)
    VALUES (datetime('now'), ?, ?, ?, ?)
    """, (data['Temperature'], data['Humidity'], data['Lights'], data['Fan']))

    # commit the changes and close the connection
    connection.commit()
    connection.close()

    # return a confirmation message
    return {"message": "Data stored"}

def calculate_average(hours):
    # connect to the sqlite database
    connection = sqlite3.connect('data.db')

    # create a cursor
    cursor = connection.cursor()

    # calculate the average temperature and humidity during the provided hours
    cursor.execute("""
    SELECT AVG(temperature), AVG(humidity)
    FROM sensor_data
    WHERE timestamp > datetime('now', '-{} hours')
    """.format(hours))  # only selects values after the hours provided

    # fetch the result
    avg_temp, avg_humidity = cursor.fetchone()

    # close the connection
    connection.close()

    # return the averages
    return {'Average Temperature': avg_temp, 'Average Humidity': avg_humidity}

def fetch_history(hours):
    # connect to the sqlite database
    connection = sqlite3.connect('data.db')

    # create a cursor
    cursor = connection.cursor()

    # only selects values after the hours provided
    cursor.execute("""
    SELECT timestamp, temperature, humidity, lights, fan
    FROM sensor_data
    WHERE timestamp > datetime('now', '-{} hours')
    """.format(hours))

    # fetch all the results
    rows = cursor.fetchall()

    # close the connection
    connection.close()

    # return the results
    return rows

def delete_history(hours):
    # connect to the sqlite database
    connection = sqlite3.connect('data.db')

    # create a cursor
    cursor = connection.cursor()

    # only selects values after the hours provided
    cursor.execute("""
    DELETE FROM sensor_data
    WHERE timestamp > datetime('now', '-{} hours')
    """.format(hours))

    # commit the changes and close the connection
    connection.commit()
    connection.close()

    # return a confirmation message
    return {"message": "Data deleted"}

def display_update():
    # connect to the sqlite database
    connection = sqlite3.connect('data.db')

    # create a cursor
    cursor = connection.cursor()

    # only selects values after the hours provided
    cursor.execute("""
    SELECT timestamp, temperature, humidity, lights, fan
    FROM sensor_data
    ORDER BY timestamp DESC
    LIMIT 1
    """)

    # fetch all the results
    rows = cursor.fetchall()

    # close the connection
    connection.close()

    message = {"Temperature": rows[0][1], "Humidity": rows[0][2], "Lights": rows[0][3], "Fan": rows[0][4]}

    # return the results
    return message
