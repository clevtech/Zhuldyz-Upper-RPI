# -*- coding: utf-8 -*-
from flask import Flask, render_template, json, request
import apiai
import random
import sys


app = Flask(__name__)


def textMessage(update):
    request = apiai.ApiAI('167a082419914df2b44700f2bcda6087').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'ZhuldyzAIbot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        print("Действие: " + str(responseJson['result']['action']))
        print("Ответ: " + str(responseJson['result']['fulfillment']['speech']))
        print("Вероятность: " + str(responseJson['result']['score']*100))
        return str(responseJson['result']['fulfillment']['speech'])
    else:
        print("Непонятно")
        return "Простите, я не поняла Вас"


@app.route('/')
def index(phrase=''):
    name = name2
    global answer
    answer2 = answer
    return render_template('index.html', **locals())


@app.route('/get_len', methods=['GET', 'POST'])
def get_len():
    if request.form['text']:
        print(request.form['text'])
        global answer
        answer = textMessage(request.form['text'])
        moods = ["Angry", "Happy", "Normal", "Sexy", "Suprised", "Thinking"]
        global name2
        name2 = moods[random.randint(0, len(moods) - 1)]
        return json.dumps({'refresh': 1})
    else:
        return json.dumps({'refresh': 0})


if __name__ == '__main__':
    name2 = 'Happy'
    answer = ' '
    app.run(debug=True)
