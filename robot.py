import cv2
import speech_recognition as sr
import socket
import sys
import random
import apiai
import json

# Work with lower RPI
def go_to_position(position, conn, MAX_BUFFER_SIZE = 4096):
    sms = position.encode("utf-8")
    conn.sendall(sms)
    return True


# End of work with lower RPI

# Interfaces block
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


# End of interfaces block


# Facial recognition block
def recognize_face():
    while True:
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        try:
            number = len(faces)
            size = [faces[0][2], faces[0][3]]
            position = [faces[0][0], faces[0][1]]
            if size[0] < 110:
                number = 0
            break
        except:
            a = 1
    return size, position, number


def see_face():
    while True:
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        try:
            position = [faces[0][0], faces[0][1]]
            if position[0] < 100:
                print("turn right")
            elif position[0] > 300:
                print("turn left")
            else:
                print("face in middle")
                return 1
        except:
            return 0
# End of facial recognition block


def listen_question():
    try:
        r = sr.Recognizer()
        #source = open(sr.Microphone())
        with sr.Microphone() as source:
            #print(source)
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)
        try:
            question = r.recognize_google(audio)
        except sr.UnknownValueError:
            question = None
    except:
        question = input("Question?: ")
    print(question)
    return question


# Talking protocol
def talking():
    size, position, number = recognize_face()
    print("Number of faces is " + str(number))
    if number > 0:
        open_phrase = "Задавайте вопросы, я вам помогу"
        send_to_display(top_conn, bot_conn, names, open_phrase, 1)
        from_display(top_conn)
        from_display(bot_conn)
        while True:
            question = listen_question()
            if question.lower() == "начинай экскурсию":
                return 2
            elif question.lower() == "пора спать":
                return 4
            elif question.lower() == "пора работать":
                return 5
            elif question:
                send_to_display(top_conn, bot_conn, names, question, 0)
                from_display(top_conn)
                from_display(bot_conn)
            else:
                size, position, number = recognize_face()
                if number < 1:
                    break
                else:
                    send_to_display(top_conn, bot_conn, names, "Пожалуйста, не спешите говорить", 1)
                    from_display(top_conn)
                    from_display(bot_conn)
    elif number == 0:
        if random.randint(1, 50) == 1:
            catch_phrase = "Пожалуйста, подходите на экскурсию по павильону казкосмос, " \
                           "я вам всё покажу, всё расскажу."
            send_to_display(top_conn, bot_conn, names, catch_phrase, 1)
            from_display(top_conn)
            from_display(bot_conn)
    return 1
# End of talking protocol


# Setup function
def setup_all():
    # Initialize OpenCV
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # WIDTH
    cap.set(4, 480)  # HEIGHT
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    return cap, face_cascade
# End of setup function


# Main function
if __name__ == '__main__':
    # Инициализация системы
    top_ip = "192.168.2.2"
    top_port = 6666
    bot_ip = "192.168.2.2"
    bot_port = 7777
    leg_ip = "192.168.2.2"
    leg_port = 5555

    top_conn, names, top_soc = start_server(top_ip, top_port)
    bot_conn, names, bot_soc = start_server(bot_ip, bot_port)
    leg_conn, names, leg_soc = start_server(leg_ip, leg_port)

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

    # Initialize protocol
    protocol = 1
    # 1 = dialogues, 2 - fair, 3 - go to position A, 4 - go charge, 5 - wake up

    while True:
        dvigai = "Пожалуйста, позвольте провести экскурсию."
        if protocol == 1:
            print("Protocol 1")
            protocol = talking()
        elif protocol == 2:
            positions = ["ab", "bc", "cd"]
            for position in positions:
                # Берет фразы историй
                with open("./" + str(position) + ".txt", "r") as file:
                    texts = file.readlines()
                go_to_position(position, leg_conn, MAX_BUFFER_SIZE=4096)
                for phrase in texts:
                    # Отправляет тебе стринг "ab", "bc" или "cd"

                    send_to_display(top_conn, bot_conn, names, phrase, 0)
                    from_display(top_conn)
                    from_display(bot_conn)
                feedback = from_display(leg_conn)
            for i in range(20):
                talking()
            protocol = 3
        elif protocol == 3:
            # Отправляет тебе стринг "a"
            position = "a"
            go_to_position(position, leg_conn, MAX_BUFFER_SIZE=4096)
            feedback = from_display(leg_conn)
            protocol = 1
        elif protocol == 4:
            position = "charge"
            go_to_position(position, leg_conn, MAX_BUFFER_SIZE=4096)
            feedback = from_display(leg_conn)
            protocol = 1
        elif protocol == 5:
            position = "from_charge"
            go_to_position(position, leg_conn, MAX_BUFFER_SIZE=4096)
            feedback = from_display(leg_conn)
            protocol = 1

