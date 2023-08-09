import socket
import json
import sqlite3
from contextlib import closing

from serverDB import store_data, calculate_average, fetch_history, display_update

# local host and port to be used
Host = '127.0.0.2'
Port = 65435


def store_data(data):
    # Connect to the data.db database created to hold information
    database_connection = sqlite3.connect('data.db')
    # Create a cursor to input data into the table
    cursor = database_connection.cursor()
    # Insert data into table
    cursor.execute("""
    INSERT INTO sensor_data (timestamp, temperature, humidity, lights, fan)
    VALUES (datetime('now'), ?, ?, ?, ?)
    """, (data['Temperature'], data['Humidity'], data['Lights'], data['Fan']))

    # Commit the changes
    database_connection.commit()

    cursor.close()
    database_connection.close()

    # Return a confirmation message
    return {"message": "Message received"}


def calculate_average(hours):
    # Connect to the SQLite database
    connection = sqlite3.connect('data.db')
    # Create a cursor
    cursor = connection.cursor()
    # Calculate the average temperature and humidity during the provided hours
    cursor.execute("""
    SELECT AVG(temperature), AVG(humidity)
    FROM sensor_data
    WHERE timestamp > datetime('now', '-{} hours')
    """.format(hours))  # Only selects values after the hours provided

    # Fetch the result
    avg_temp, avg_humidity = cursor.fetchone()

    cursor.close()
    connection.close()

    # Return the averages
    return {'Average Temperature': avg_temp, 'Average Humidity': avg_humidity}


def fetch_history(hours):
    # Connect to the data.db database created to hold information
    connection = sqlite3.connect('data.db')
    # Create a cursor
    cursor = connection.cursor()
    # Only selects values after the hours provided
    cursor.execute("""
    SELECT timestamp, temperature, humidity, lights, fan
    FROM sensor_data
            WHERE timestamp > datetime('now', '-{} hours')
            """.format(hours))

    # Fetch all the results
    rows = cursor.fetchall()

    history = []
    # Create a list of dictionaries to represent the data
    for data_row in rows:
        timestamp = data_row[0]
        temperature = data_row[1]
        humidity = data_row[2]
        lights = data_row[3]
        fan = data_row[4]

        new_entry_dict = {
            'timestamp': timestamp,
            'temperature':temperature,
            'humidity': humidity,
            'lights': lights,
            'fan': fan
        }

        history.append(new_entry_dict)

    cursor.close()
    connection.close()

    # Return the history
    return history


def start_server():
    # Create and rename socket to binded_socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binded_socket:
        # Bind the socket to the local host and selected port
        binded_socket.bind((Host, Port))

        # Listen for connections
        binded_socket.listen()

        while True:
            # Accept a connection
            connection, address = binded_socket.accept()

            with connection:
                # Receive data
                data_received = connection.recv(1024)
                if data_received:
                    print(data_received)

                # If not data received, restart loop
                if not data_received:
                    continue

                # Parse JSON data
                data_received = json.loads(data_received.decode())
                print (data_received)

                if 'Average' in data_received:
                    # Calculate the average based on the hours requested
                    hours_requested = data_received['Average']
                    averages = calculate_average(hours_requested)
                    print('Averages calculated')

                    # Send newly calculated average back to user
                    connection.sendall(json.dumps(averages).encode())
                    print('Averages sent')

                elif 'History' in data_received:
                    # Fetch the history
                    hours_requested = data_received['History']
                    history = fetch_history(hours_requested)
                    print('History fetched')

                    # Check if history is empty
                    if not history:
                        history = {'Issue': 'Problem with the hours requested. No values within that time frame'}

                    # Send the history back to the client
                    connection.sendall(json.dumps(history).encode())
                    print('History sent')

                elif 'update_display' in data_received:
                    print("Sending display update")
                    message = display_update()
                    print (message)
                    connection.sendall(json.dumps(message).encode())
                    print("Display update sent")

                else:
                    # Store data into database
                    store_data(data_received)
                    print('Data stored')

                    # Send confirmation to client data was received
                    connection.sendall(json.dumps({"message": "Message received"}).encode())
                    print('Confirmation sent')


if __name__ == "__main__":
    start_server()
