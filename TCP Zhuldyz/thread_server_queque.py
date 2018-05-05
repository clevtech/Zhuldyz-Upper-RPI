import socket
import sys
import traceback
from threading import Thread
from queue import Queue


q = Queue(maxsize=0)


def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    while True:
        # the input is in bytes, so decode it
        input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

        # MAX_BUFFER_SIZE is how big the message can be
        # this is test if it's sufficiently big
        siz = sys.getsizeof(input_from_client_bytes)
        if siz >= MAX_BUFFER_SIZE:
            print("The length of input is probably too long: {}".format(siz))

        # decode input and strip the end of line
        input_from_client = input_from_client_bytes.decode("utf8").rstrip()
        print(input_from_client)
        data = q.get()
        res = data
        print("Result of processing {} is: {}".format(input_from_client, res))

        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client
        # conn.close()  # close connection
        # print('Connection ' + ip + ':' + port + " ended")


def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(("192.168.8.104", 6666))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    # Start listening on socket
    soc.listen(2)
    print('Socket now listening')
    # this will make an infinite loop needed for
    # not reseting server for every client

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terrible error!")
            traceback.print_exc()
            soc.close()


Thread(target=start_server()).start()
print("Server started")
while True:
    print("Give me answer, boy!")
    q.put(input("what>>>"))

