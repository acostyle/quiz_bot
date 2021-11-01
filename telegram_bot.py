import json
import logging
import random
from functools import partial

from redis import Redis
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from environments import (
    TELEGRAM_TOKEN,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
    CHAT_ID,
)
from parse_quiz import parse_quiz_file


logger = logging.getLogger('bot_logger')

QUIZ_CONTENT = parse_quiz_file('src/')
QUESTION = 0
ANSWER = 1


def start(bot, update):
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        'Привет, я бот для викторин!',
        reply_markup=reply_markup
    )

    return QUESTION


def send_question(bot, update, db):
    logger.info(
        'Пользователь {0} получил новый вопрос.'.format(
            update.message.from_user.first_name
        )
    )
    question, answer = random.choice(list(QUIZ_CONTENT.items()))

    db.set(update.effective_chat.id, json.dumps([question, answer]))
    update.message.reply_text(question)

    return ANSWER


def check_answer(bot, update, db):
    question_with_answer = db.get(update.effective_user.id).decode('utf-8')
    question, answer = json.loads(question_with_answer)

    if update.message.text == 'Новый вопрос':
        update.message.reply_text(
            'Вы не ответили на старый вопрос!\n{0}'.format(question),
        )
    elif update.message.text == 'Сдаться':
        update.message.reply_text('Правильный {0}'.format(answer))
        return QUESTION
    elif update.message.text.lower() in answer.lower():
        update.message.reply_text('Верно! {0}'.format(answer))
        return QUESTION
    else:
        update.message.reply_text(
            'Ответ неверный! Попробуйте еще раз или сдайтесь!',
        )


def error(update, error):
    logger.warning('Update "{0}" caused error "{1}"'.format(update, error))


def cancel(bot, update):
    user = update.message.from_user
    logger.info('Пользователь {0} сдался.'.format(user.first_name))
    update.message.reply_text(
        'Возвращайся еще :)', reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    redis_db = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION: [
                MessageHandler(
                    Filters.regex('^Новый вопрос$'),
                    partial(send_question, db=redis_db),
                ),
            ],
            ANSWER: [
                MessageHandler(
                    Filters.text,
                    partial(check_answer, db=redis_db),
                ),
            ],
        },
        fallbacks=[MessageHandler(Filters.text, cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
