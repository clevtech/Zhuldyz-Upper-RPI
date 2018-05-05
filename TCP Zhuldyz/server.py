import socket


def server_test():
    host = "192.168.8.104"
    port = 6666
    Darik = socket.socket()
    Darik.bind((host, port))
    Darik.listen(1)
    conn, addr = Darik.accept()
    print("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Darik: " + str(data))
        data = "Pong!"
        print("Bauka: " + str(data))
        conn.send(data.encode())
    conn.close()


if __name__ == '__main__':
    server_test()

