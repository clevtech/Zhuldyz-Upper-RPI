import socket
from time import sleep


def server_test():
    host = "192.168.1.103"
    port = 5555
    Batyr = socket.socket()
    Batyr.bind((host, port))
    Batyr.listen(1)
    conn, addr = Batyr.accept()
    print("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Batyr: " + str(data))
        data = input("Data to send: ")
        print("Bauka: " + str(data))
        conn.send(data.encode())
        sleep(10)
    conn.close()


if __name__ == '__main__':
    server_test()

