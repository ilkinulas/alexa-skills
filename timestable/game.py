import logging

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logger = logging.getLogger("flask_ask")
logger.setLevel(logging.DEBUG)


@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("YesIntent")
def next_round():
    _, _, msg = new_question(randint(0, 9), randint(0, 9))
    return question(msg)


@ask.intent("AnswerIntent", convert={'response': int})
def answer(response):
    a = session.attributes['first_number']
    b = session.attributes['second_number']

    if response == a * b:
        _, _, msg = new_question(randint(0, 9), randint(0, 9))
        msg = "{} {}".format(render_template("win"), msg)
    else:
        _, _, prev_question = new_question(a, b)
        msg = "{} {}".format(render_template("lose", response=response), prev_question)

    return question(msg)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)


def new_question(first_number, second_number):
    question_msg = render_template(
        'question',
        first_number=first_number,
        second_number=second_number)

    session.attributes['first_number'] = first_number
    session.attributes['second_number'] = second_number
    return first_number, second_number, question_msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=('certificate.pem', 'private-key.pem'))
