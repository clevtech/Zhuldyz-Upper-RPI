import random
import apiai
import json
import cv2
from gtts import gTTS
import os
import speech_recognition as sr
import tkinter
from PIL import Image, ImageTk


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
            question = r.recognize_google(audio, language="ru-RU")
        except sr.UnknownValueError:
            question = None
    except:
        question = input("Question?: ")
    print(question)
    return question


def show_emotion(emotion):
    # img2 = cv2.imread("./static/" + str(emotion) + ".png")
    # cv2.imshow("window", img2)
    # pilImage = Image.open("./static/" + str(emotion) + ".png")
    print("./static/" + str(emotion) + ".png")
    return True


def say_answer(answer):
    tts = gTTS(text=answer, lang='ru', slow=False)
    tts.save("answer.mp2")
    os.system("mpg321 answer.mp2")
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
            else:
                print("face in middle")
                return 1
        except:
            return 0


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
            print("Protocol 1")
            protocol = talking()
        elif protocol == 2:
            break

