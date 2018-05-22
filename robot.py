import speech_recognition as sr
import socket
import sys
import random
import apiai
import json
from time import sleep
import RPi.GPIO as GPIO


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
    print("Question is " + str(phrase))
    res, res2 = give_answer(phrase, names, types)
    print("Result is " + str(res))

    vysl = res.encode("utf8")  # encode the result string
    top_conn.sendall(vysl)  # send it to client
    vysl2 = res2.encode("utf8")  # encode the result string
    bot_conn.sendall(vysl2)  # send it to client
    print("Send to displays")


def from_display(conn, MAX_BUFFER_SIZE = 126000):

    # the input is in bytes, so decode it
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    siz = sys.getsizeof(input_from_client_bytes)
    if siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    # decode input and strip the end of line
    input_from_client = input_from_client_bytes.decode("utf8").rstrip()
    print("Feedback from TCP is " + str(input_from_client))
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


def listen_question():
    try:
        r = sr.Recognizer()
        #source = open(sr.Microphone())
        with sr.Microphone() as source:
            #print(source)
            r.adjust_for_ambient_noise(source)

            try:
                print("Say something!")
                audio = r.listen(source)
                print("You said")
            except:
                return None
        try:
            question = r.recognize_google(audio, language="ru-RU")
        except sr.UnknownValueError:
            question = None
    except:
        question = input("Question?: ")
    print(question)
    return question


def Okay_robot():
    ups = 0
    r = sr.Recognizer()
    #source = open(sr.Microphone())
    with sr.Microphone() as source:
        #print(source)
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        try:
            audio = r.listen(source, timeout=2)
            print("You said")
        except:
            return 0
    try:
        question = r.recognize_google(audio, language="ru-RU")
        print(question)
        list_of_questions = question.split()
        print(list_of_questions)
        list_of_phrases = ["жулдыз", "жолдас", "елдос", "шолпан", "юлдуз", "ердос", "робот", "гид", "инвините",
                           "простите", "привет", "здравствуйте", "извиняюсь", "подруга", "друг", "желдор", "желтый",
                           "желтая", "жёлтый", "жёлтая"]
        for phrase in list_of_phrases:
            for question in list_of_questions:
                if str(phrase).lower() == str(question).lower():
                    print("Start a party")
                    return 1
                else:
                    ups = 1
    except sr.UnknownValueError:
        return 0
    if ups == 1:
        return 0


def SetAngle(angle):
        duty = int(angle) / 18 + 2
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(duty)

        sleep(1)
        GPIO.output(3, False)
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(0)
        sleep(1)
        GPIO.output(3, False)


# Talking protocol
def talking():
    # Сюда
    number = Okay_robot()
    print("Number of faces is " + str(number))
    if int(number) == 1:
        open_phrase = "Меня зовут Жулдыз, и я робот гид"
        print(open_phrase)
        send_to_display(top_conn, bot_conn, names, open_phrase, 1)
        from_display(top_conn)
        from_display(bot_conn)
        a = 0
        while True:
            question = listen_question()
            print("Question is " + str(question))

            if question:
                if question.lower() == "экскурсия":
                    return 2
                send_to_display(top_conn, bot_conn, names, question, 0)
                from_display(top_conn)
                from_display(bot_conn)
            else:
                sleep(1)
                a = a + 1
                if a == 2:
                    return 1
                send_to_display(top_conn, bot_conn, names, "Простите, я вас не услышала", 1)
                from_display(top_conn)
                from_display(bot_conn)


    else:
        print("waiting loop")
        if random.randint(1, 50) == 1:
            catch_phrase = "Пожалуйста, подходите на экскурсию по павильону казкосмос, " \
                           "я вам всё покажу, всё расскажу."
            send_to_display(top_conn, bot_conn, names, catch_phrase, 1)
            from_display(top_conn)
            from_display(bot_conn)
    return 1
# End of talking protocol


# Main function
if __name__ == '__main__':
    GPIO.cleanup()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    pwm = GPIO.PWM(3, 50)
    pwm.start(0)
    SetAngle(90)
    SetAngle(90)

    # Инициализация системы
    top_ip = input("Your ip is: ")
    top_port = 6666
    bot_ip = top_ip
    bot_port = 7777
    leg_ip = top_ip
    leg_port = 5555
    print("Starting face tcp")
    top_conn, names, top_soc = start_server(top_ip, top_port)
    print("Starting boob tcp")
    bot_conn, names, bot_soc = start_server(bot_ip, bot_port)
    print("Starting leg tcp")
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
        try:
            if protocol == 1:
                print("Protocol 1:")
                protocol = talking()
            elif protocol == 2:
                positions = ["ab", "bc"]
                for position in positions:
                    print("Position is " + str(position))
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
            else:
                position = "a"
                go_to_position(position, leg_conn)
                feedback = from_display(leg_conn)
                protocol = 1
        except:
            print("Some problem")

