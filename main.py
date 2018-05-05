import random
import apiai
import json
import cv2
import os
import speech_recognition as sr


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
        answer = "Простите, я Вас не поняла. Можете перефразировать, я только учусь."
        emotion = "Thinking"
    return answer, emotion


def listen_question():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            duration = 1  # second
            freq = 440  # Hz
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
            audio = r.listen(source)
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
        try:
            question = r.recognize_google(audio, language="ru-RU")
        except sr.UnknownValueError:
            question = None
    except:
        question = input("Question?: ")
    return question


def show_emotion(emotion):
    # Send socks
    return True


def say_answer(answer):
    # Send socks
    return True


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
            break
        except:
            a = 1
    return True


def location():

    return True


if __name__ == '__main__':
    # Initialize OpenCV
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) #WIDTH
    cap.set(4, 480) #HEIGHT
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 1 = dialogues, 2 - fair, 3 - go to position A, 4 - go charge
    protocol = 1
    emotions = ["Angry", "Happy", "Normal", "Sexy", "Suprised", "Thinking"]
    while True:
        show_emotion("Normal")
        if protocol == 1:
            size, position, number = recognize_face()
            if number > 3:
                fair_phrase = "Нас уже много, давайте начнем экскурсию! Следуйте за мной, пожалуйста."
                show_emotion("Happy")
                protocol = 2
            elif number > 0:
                open_phrase = "Здраствуйте, меня зовут Жулдыз. Добро пожаловать на павильон Казкосмос. Чем помочь?"
                say_answer(open_phrase)
                while True:
                    question = listen_question()
                    if question:
                        answer, emotion = give_answer(question)
                        see_face()
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
                            say_answer("Повторите, пожалуйста, Вас не слышно.")
            elif number == 0:
                if random.randint(1, 5) == 1:
                    catch_phrase = "Пожалуйста, подходите на экскурсию по павильону казкосмос, " \
                                   "я вам всё покажу, всё расскажу."
                    say_answer(catch_phrase)
        elif protocol == 2:
            break

