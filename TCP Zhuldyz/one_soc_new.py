import socket
import sys
import traceback
import random
import apiai
import json


def give_answer(question, names, types = 0):
    if types == 0:
        request = apiai.ApiAI('167a082419914df2b44700f2bcda6087').text_request() # Токен API к Dialogflow
        request.lang = 'ru' # На каком языке будет послан запрос
        request.session_id = 'ZhuldyzAIbot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = question # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        information = "clev"
        emotion = "Happy"
        if response:
            answer = str(responseJson['result']['fulfillment']['speech'])
            if str(responseJson['result']['action']) == "smalltalk.user.angry":
                emotion = "Angry"
            elif str(responseJson['result']['action']) == "smalltalk.user.loves_agent":
                emotion = "Sexy"
            elif str(responseJson['result']['action']) == "smalltalk.agent.beautiful":
                emotion = "Happy"
            elif str(responseJson['result']['action']) == "smalltalk.greetings.bye":
                emotion = "Suprised"
            else:
                emotion = "Happy"
            for name in names:
                if str(responseJson['result']['metadata']['intentName']) == name:
                    information = str(responseJson['result']['metadata']['intentName'])
                    break
                else:
                    information = "clev"
        else:
            answer = "Простите, я Вас не поняла. Можете перефразировать, я только учусь."
            emotion = "Thinking"
            information = "clev"

        message = emotion + "#ru-RU#" + answer
        messagelow = information + "#None#None"
    else:
        message = "Normal#ru-RU#" + question
        messagelow = "clev#None#None"
    return message, messagelow


# types_off = 0 for face, 1 for boobs; types = 0 for clever answer, 1 for just say;
def send_to_display(top_conn, bot_conn, names, phrase, types):
    res, res2 = give_answer(phrase, names, types)

    vysl = res.encode("utf8")  # encode the result string
    top_conn.sendall(vysl)  # send it to client
    vysl2 = res2.encode("utf8")  # encode the result string
    bot_conn.sendall(vysl2)  # send it to client


def from_display(conn, MAX_BUFFER_SIZE = 4096):

    # the input is in bytes, so decode it
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    siz = sys.getsizeof(input_from_client_bytes)
    if siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    # decode input and strip the end of line
    input_from_client = input_from_client_bytes.decode("utf8").rstrip()
    return input_from_client


def start_server(ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket 1 created')

    with open("./list.txt", "r") as listik:
        files = listik.readlines()
        names = []
        for fil in files:
            names.append(fil.replace('\n', '').replace('\r', ''))

    try:
        soc.bind((ip, port))
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
    return conn, names, soc


def speak_with():

    # Инициализация системы
    top_ip = "192.168.2.2"
    top_port = 6666
    bot_ip = "192.168.2.2"
    bot_port = 7777

    top_conn, names, top_soc = start_server(top_ip, top_port)
    bot_conn, names, bot_soc = start_server(bot_ip, bot_port)

    if from_display(bot_conn) == "Hello":
        print("Boobs are connected")
        if from_display(top_conn) == "Hello":
            print("Face is connected")
            send_to_display(top_conn, bot_conn, names, "Инициализация всей системы, протокол Зарождение", 1)
            if from_display(top_conn):
                if from_display(bot_conn):
                    send_to_display(top_conn, bot_conn, names, "Завершение протокола Зарождение, "
                                                               "я родилась, протокол собеседник", 1)
                    from_display(top_conn)
                    from_display(bot_conn)

    # Инициализация закончена


    while True:
        try:
            phrase = input("Phrase")
            print("Answer")
            send_to_display(top_conn, bot_conn, names, phrase, 0)
            print("From face: " + str(from_display(top_conn)))
            print("From boobs: " + str(from_display(bot_conn)))
        except:
            print("Terrible error!")
            traceback.print_exc()
            top_soc.close()
            bot_soc.close()


speak_with()