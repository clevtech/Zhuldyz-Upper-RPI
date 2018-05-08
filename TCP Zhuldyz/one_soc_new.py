import socket
import sys
import traceback
import random


def upper_monitor():
    examples = ["Normal#ru-RU#Здраствуйте, меня зовут Жулдз, я робот гид", "Happy#ru-RU#Я так рада что вы тут",
                "Sad#ru-RU#Простите, я вас не поняла, можете, пожалуйста, перефразировать",
                "Angry#ru-RU#Алё, тупое быдло, дай дорогу, королева идет", "Sexy#en-GB#Let`s do it, baby",
                "Normal#None#None"]
    message = examples[random.randint(0, 5)]
    print(message)
    return message


def lower_monitor():
    examples = ["Kazkosmos", "KGS", "Matrix"]
    picture = examples[random.randint(0, 3)]
    print(picture)
    return picture


def client_thread(types_off, conn, ip, port, MAX_BUFFER_SIZE = 4096):

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
    if types_off == 1:
        res = upper_monitor()
    else:
        res = lower_monitor()
    print("Result of processing {} is: {}".format(input_from_client, res))

    vysl = res.encode("utf8")  # encode the result string
    conn.sendall(vysl)  # send it to client
    # conn.close()  # close connection
    # print('Connection ' + ip + ':' + port + " ended")

def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket 1 created')

    try:
        soc.bind(("192.168.8.104", 6666))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    # Start listening on socket
    soc.listen(1)
    print('Socket now listening')
    # this will make an infinite loop needed for
    # not reseting server for every client
    conn, addr = soc.accept()
    ip, port = str(addr[0]), str(addr[1])
    print('Accepting connection 1 from ' + ip + ':' + port)
    while True:
        try:
            print("First one:")
            client_thread(1, conn, ip, port)
        except:
            print("Terrible error!")
            traceback.print_exc()
            soc.close()

start_server()

