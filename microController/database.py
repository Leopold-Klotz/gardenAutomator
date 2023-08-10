import csv
import os

# Define the file paths for CSV files
MEASUREMENT_DATA_FILE = 'measurement_data.csv'
AVERAGE_DATA_FILE = 'average_data.csv'

async def setup_db():
    # Create the 'measurement_data' file if it doesn't exist
    if not os.path.exists(MEASUREMENT_DATA_FILE):
        with open(MEASUREMENT_DATA_FILE, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['temperature', 'humidity'])

    # Create the 'average_data' file if it doesn't exist
    if not os.path.exists(AVERAGE_DATA_FILE):
        with open(AVERAGE_DATA_FILE, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['temperature', 'humidity', 'lights', 'fan'])

async def store_minute_data(measurements):
    with open(MEASUREMENT_DATA_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(measurements)

async def store_hourly_data(lights, fan):
    # Read the measurement data file
    with open(MEASUREMENT_DATA_FILE, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Calculate the average temperature and humidity
    if len(data) >= 60:
        avg_temp = sum(float(row[0]) for row in data) / len(data)
        avg_humidity = sum(float(row[1]) for row in data) / len(data)

        # Append the average data to the average data file
        with open(AVERAGE_DATA_FILE, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([avg_temp, avg_humidity, lights, fan])

        # Clear the measurement data file
        with open(MEASUREMENT_DATA_FILE, 'w') as f:
            pass

async def fetch_avg_data():
    rows = []
    if os.path.exists(AVERAGE_DATA_FILE):
        with open(AVERAGE_DATA_FILE, 'r') as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
    return rows

async def delete_avg_data():
    if os.path.exists(AVERAGE_DATA_FILE):
        os.remove(AVERAGE_DATA_FILE)
