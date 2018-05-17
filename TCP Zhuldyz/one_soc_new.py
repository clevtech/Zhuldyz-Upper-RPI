import socket
import sys
import traceback
import random
import apiai
import json


def give_answer(question):
    request = apiai.ApiAI('167a082419914df2b44700f2bcda6087').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'ZhuldyzAIbot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = question # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
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
            try:
                emotion = str(responseJson['result']['metadata']['intentName'])
                print(responseJson)
            except:
                emotion = "Happy"
    else:
        answer = "Простите, я Вас не поняла. Можете перефразировать, я только учусь."
        emotion = "Thinking"
    return answer, emotion


def upper_monitor():
    #examples = ["clev#ru-RU#Здраствуйте, меня зовут Жулдыз, я робот гид", "Happy#ru-RU#Я так рада что вы тут"]
    phrase = input("What to ask?")
    answer, emotion = give_answer(phrase)
    message = emotion + "#ru-RU#" + answer
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
        soc.bind(("192.168.2.2", 6666))
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

