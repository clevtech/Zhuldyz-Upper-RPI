import socket


def Main():
    host = '192.168.8.104'
    port = 7777

    mySocket = socket.socket()
    mySocket.connect((host, port))
    message = input(" -> ")
    while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print('Received from server: ' + data)
        message = input(" -> ")


    mySocket.close()


if __name__ == '__main__':
    Main()

