import json
import logging
import random

import vk_api as vk
from redis import Redis
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from environments import VK_TOKEN, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from parse_quiz import parse_quiz_file


logger = logging.getLogger('bot_logger')

QUIZ_CONTENT = parse_quiz_file('src/')


def send_message(event, vk_api, keyboard, message_text):
    return vk_api.messages.send(
        user_id=event.user_id,
        message=message_text,
        keyboard=keyboard,
    )


def make_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    return keyboard


def send_question(event, vk_api, db, keyboard):
    logger.info(
        'Пользователь {0} получил новый вопрос.'.format(event.user_id)
    )
    question, answer = random.choice(list(QUIZ_CONTENT.items()))

    db.set(event.user_id, json.dumps([question, answer]))
    send_message(
        user_id=event.user_id,
        message=question,
        keyboard=keyboard.get_keyboard(),
    )


def check_user_message(event, vk_api, db, keyboard):
    question_with_answer = db.get(event.user_id).decode('utf-8')
    question, answer = json.loads(question_with_answer)

    if event.text.lower() in answer.lower():
        send_message(
            user_id=event.user_id,
            message='Верно! {0}'.format(answer),
            keyboard=keyboard.get_keyboard(),
        )
    else:
        send_message(
            user_id=event.user_id,
            message='Ответ неверный! Попробуйте еще раз или сдайтесь!',
            keyboard=keyboard.get_keyboard(),
        )


def cancel(event, vk_api, keyboard):
    logger.info('Пользователь {0} сдался.'.format(event.user_id))
    send_message(
        user_id=event.user_id,
        message='Возвращайся еще :)',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def main():
    vk_session = vk.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    redis_db = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )

    keyboard = make_keyboard()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text in ['Здравствуйте', 'Приветствую', 'Привет']:
                send_message(
                    user_id=event.user_id,
                    keyboard=keyboard.get_keyboard(),
                    message='Привет. Это бот с викторинами.\
                Нажми на кнопку – Новый вопрос',
                )
            elif event.text == 'Новый вопрос':
                send_question(event, vk_api, redis_db, keyboard)
            elif event.text == 'Сдаться':
                cancel(event, vk_api, keyboard)
            else:
                check_user_message(event, vk_api, redis_db, keyboard)


if __name__ == '__main__':
    main()
