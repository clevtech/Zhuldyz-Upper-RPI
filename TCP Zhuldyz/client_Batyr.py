import socket
# Sample socket app for connect from lower RPI to higher RPI
# Done by @Naboo to @Batyr


# Function to listen socket connection
def read_from_socket(mySocket):
    # data is decoded message from higher RPI
    data = mySocket.recv(1024).decode()
    # return message data
    return data


# Send to socket
def send_to_socket(mySocket, message):
    try:
        # Sends socket data message
        mySocket.send(message.encode())
        # If ok - return 1
        return 1
    except:
        # If problem - return 0
        return 0


def Main():
    # Connect to Higher RPI
    host = '192.168.8.104' # Here goes IP address of the Higher RPI
    port = 9999 # It is socket port of the higher RPI
    mySocket = socket.socket() # Creating socket
    mySocket.connect((host, port)) # Defying socket ip and port

    message = "pingRPI" # Sending to higher RPI that lower RPI is connected
    # Sending it
    send_to_socket(mySocket, message)

    # Receiving data
    data = read_from_socket(mySocket)

    # Printing received message
    print(data)


    # Closing socket connection
    mySocket.close()


if __name__ == '__main__':
    Main()

