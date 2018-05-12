import random
import apiai
import json
import cv2
import speech_recognition as sr
import socket
import re


# Work with lower RPI
def go_to_position(position):
    return True


# End of work with lower RPI

# Interfaces block
def connect_to_interfaces():

    # Create sockets for each RPI

    # Create socket for face
    face = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    face.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Face created')

    # Create socket for boobs
    boobs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    boobs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Boobs created')

    # Create socket for legs
    legs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    legs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Legs created')

    # Create list of them
    sockets = [face, boobs, legs]


    try:
        face.bind(("192.168.8.104", 6666))
        boobs.bind(("192.168.8.104", 7777))
        legs.bind(("192.168.8.104", 5555))
        print('Sockets bind complete')
    except:
        print('Bind failed. Error')


    # Start listening on socket
    for el in sockets:
        el.listen(1)
    print('Socket now listening')

    conn_face, addr_face = face.accept()
    ip_face, port_face = str(addr_face[0]), str(addr_face[1])
    print('Accepting connection 1 from ' + ip_face + ':' + port_face)
    conn_boobs, addr_boobs = boobs.accept()
    ip_boobs, port_boobs = str(addr_boobs[0]), str(addr_boobs[1])
    print('Accepting connection 2 from ' + ip_boobs + ':' + port_boobs)
    conn_legs, addr_legs = legs.accept()
    ip_legs, port_legs = str(addr_legs[0]), str(addr_legs[1])
    print('Accepting connection 2 from ' + ip_legs + ':' + port_legs)

    return conn_face, addr_face, ip_face, port_face, face, conn_boobs, \
           addr_boobs, ip_boobs, port_boobs, boobs, conn_legs, addr_legs, \
           ip_legs, port_legs, legs


def receive_interface_feedback(conn, MAX_BUFFER_SIZE = 4096):
    # the input is in bytes, so decode it
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
    # decode input and strip the end of line
    input_from_client = input_from_client_bytes.decode("utf8").rstrip()
    return input_from_client


def send_interface_command(texts, emotion, conn):
    res = emotion + "#" + detect_lang(texts) + "#" + texts
    vysl = res.encode("utf8")  # encode the result string
    conn.sendall(vysl)  # send it to client
    return True
# End of interfaces block


# Additional modules
def detect_lang(texts):
    if bool(re.search('[а-яА-Я]', texts)):
        return "ru-RU"
    else:
        return "en-GB"
# End of additional interfaces block


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



# Speech block
def give_answer(question):
    request = apiai.ApiAI('167a082419914df2b44700f2bcda6087').texts_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'ZhuldyzAIbot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = question # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        answer = str(responseJson['result']['fulfillment']['speech'])
        if str(responseJson['result']['action']) == "smalltalk.agent.annoying":
            emotion = "Angry"
        elif str(responseJson['result']['action']) == "smalltalk.user.loves_agent":
            emotion = "Sexy"
        elif str(responseJson['result']['action']) == "smalltalk.agent.beautiful":
            emotion = "Happy"
        elif str(responseJson['result']['action']) == "smalltalk.greetings.bye":
            emotion = "Suprised"
        else:
            emotion = "Happy"
    else:
        answer = "Простите, я Вас не поняла. Можете перефразировать, пожалуйста."
        emotion = "Thinking"
    return answer, emotion


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


def show_emotion(emotion):


    return True


def say_answer(answer):


    return True
# End of speech block


# Talking protocol
def talking():
    size, position, number = recognize_face()
    print("Number of faces is " + str(number))
    if number > 3:
        fair_phrase = "Нас уже много, давайте начнем экскурсию! Следуйте за мной, пожалуйста."
        say_answer(fair_phrase)
        show_emotion("Happy")
        protocol = 2
        return protocol
    elif number > 0:
        open_phrase = "Здравствуйте, меня зовут Жулдыз, чем вам помочь?"
        say_answer(open_phrase)
        while True:
            question = listen_question()
            if question:
                answer, emotion = give_answer(question)
                is_face = see_face()
                if is_face == 0:
                    break
                show_emotion(emotion)
                say_answer(answer)
                size, position, number = recognize_face()
                if number < 1:
                    break
            else:
                size, position, number = recognize_face()
                if number < 1:
                    break
                else:
                    say_answer("Пожалуйста, не спешите")
    elif number == 0:
        if random.randint(1, 15) == 1:
            catch_phrase = "Пожалуйста, подходите на экскурсию по павильону казкосмос, " \
                           "я вам всё покажу, всё расскажу."
            say_answer(catch_phrase)
    return 1
# End of talking protocol


# Setup function
def setup_all():
    # Initialize OpenCV
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # WIDTH
    cap.set(4, 480)  # HEIGHT
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    conn_face, addr_face, ip_face, port_face, face, conn_boobs, \
    addr_boobs, ip_boobs, port_boobs, boobs, conn_legs, addr_legs, \
    ip_legs, port_legs, legs = connect_to_interfaces()

    return cap, face_cascade, conn_face, addr_face, ip_face, port_face, face, conn_boobs, \
           addr_boobs, ip_boobs, port_boobs, boobs, conn_legs, addr_legs, \
           ip_legs, port_legs, legs
# End of setup function


# Main function
if __name__ == '__main__':
    # Initialize variables
    cap, face_cascade, conn_face, addr_face, ip_face, port_face, face, conn_boobs, \
           addr_boobs, ip_boobs, port_boobs, boobs, conn_legs, addr_legs, \
           ip_legs, port_legs, legs, = setup_all()

    # Initialize protocol
    protocol = 1
    # 1 = dialogues, 2 - fair, 3 - go to position A, 4 - go charge

    while True:
        show_emotion("Normal")
        if protocol == 1:
            print("Protocol 1")
            protocol = talking()
        elif protocol == 2:
            break

