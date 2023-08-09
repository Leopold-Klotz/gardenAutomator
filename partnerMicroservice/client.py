import socket
import json

# Set local host and pick port to use
HOST = 'localhost'
PORT = 65435

# Create a socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    # Connect to the socket/server
    socket.connect((HOST, PORT))

    data = {
        'Store': 'Store1',
        'Temperature': 11,
        'Humidity': 5,
        'Lights': False,
        'Fan': True
    }

    # data = {
    #     'Average': 1
    # }

    data = {
        'History': 1
    }

    # Send JSON data
    socket.sendall(json.dumps(data).encode())
    message = socket.recv(1026)
    dec_med = message.decode()
    final_mes = json.loads(dec_med)
    print(final_mes)


