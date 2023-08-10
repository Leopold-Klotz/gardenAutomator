import os

# Path to the CSV files
MEASUREMENTS_CSV = 'measurement_data.csv'
AVERAGE_CSV = 'average_data.csv'

async def setup_db():
    # Create or overwrite the measurement_data.csv file
    with open(MEASUREMENTS_CSV, 'w') as file:
        file.write('temperature,humidity\n')

    # Create or overwrite the average_data.csv file
    with open(AVERAGE_CSV, 'w') as file:
        file.write('temperature,humidity,lights,fan\n')

async def store_second_data(measurements):
    # Append measurements to the measurement_data.csv file
    with open(MEASUREMENTS_CSV, 'a') as file:
        file.write(','.join(map(str, measurements)) + '\n')

    print("Stored second data:", measurements)  # Print when storing second data
    
    return measurements  # Return the measurements

async def store_minute_data(lights, fan):
    # Read measurement data from the measurement_data.csv file
    with open(MEASUREMENTS_CSV, 'r') as file:
        lines = file.readlines()[1:]  # Skip the header line
        count = len(lines)
        if count >= 60:
            # Calculate the average temperature and humidity
            sum_temp = sum(float(line.split(',')[0]) for line in lines)
            sum_humidity = sum(float(line.split(',')[1]) for line in lines)
            avg_temp = sum_temp / count
            avg_humidity = sum_humidity / count

            # Append the average data to the average_data.csv file
            with open(AVERAGE_CSV, 'a') as avg_file:
                avg_file.write(f'{avg_temp},{avg_humidity},{lights},{fan}\n')

            # Clear the measurement_data.csv file
            os.remove(MEASUREMENTS_CSV)
            with open(MEASUREMENTS_CSV, 'w') as new_file:
                new_file.write('temperature,humidity\n')

            print("Stored minute data:", avg_temp, avg_humidity, lights, fan)  # Print when storing minute data

async def fetch_avg_data():
    print("in fetch avg")
    # Read average data from the average_data.csv file
    data = []
    with open(AVERAGE_CSV, 'r') as file:
        print("post open")
        lines = file.readlines()[1:]  # Skip the header line
        for line in lines:
            parts = line.strip().split(',')
            temp = float(parts[0])
            humidity = float(parts[1])
            lights = parts[2] == 'True'
            fan = parts[3] == 'True'
            data.append((temp, humidity, lights, fan))
    return data


async def delete_avg_data():
    # Delete the average_data.csv file
    os.remove(AVERAGE_CSV)
    with open(AVERAGE_CSV, 'w') as file:
        file.write('temperature,humidity,lights,fan\n')

