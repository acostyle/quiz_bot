from functools import partial
from queue import Queue
from redis import Redis
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import logging
from environs import Env
import random
import json

from parse_quiz import parse_quiz_file

env = Env()
env.read_env()

TELEGRAM_TOKEN = env.str('TELEGRAM_API_TOKEN')
CHAT_ID = env.int('CHAT_ID')
REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT')
REDIS_PASSWORD = env.str('REDIS_PASSWORD')

QUIZ_CONTENT = parse_quiz_file()
QUESTION = 0
ANSWER = 1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(
        chat_id=CHAT_ID,
        text='Я – бот для викторин',
        reply_markup=reply_markup
    )

    return QUESTION


def send_question(bot, update, db):
    """Send to the user question."""
    question, answer = random.choice(list(QUIZ_CONTENT.items()))

    db.set(update.effective_chat.id, json.dumps([question, answer]))
    update.message.reply_text(question)

    return ANSWER


def check_answer(bot, update, db):
    question_with_answer = db.get(update.effective_user.id).decode('utf-8')
    
    question, answer = json.loads(question_with_answer)
    print(answer)   

    if update.message.text == 'Новый вопрос':
        update.message.reply_text(
            f'Вы не ответили на старый вопрос!\n{question}')
    elif update.message.text == 'Сдаться':
        update.message.reply_text(f'Правильный {answer}')
        return QUESTION
    elif update.message.text.lower() in answer.lower():
        update.message.reply_text(f"Верно! {answer}")
        return QUESTION
    else:
        update.message.reply_text(
            "Ответ неверный! Попробуйте еще раз или сдайтесь!")


def error(update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
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
            QUESTION: [MessageHandler(Filters.regex('^Новый вопрос$'), partial(send_question, db=redis_db))],
            ANSWER: [MessageHandler(Filters.text, partial(check_answer, db=redis_db))],
        },
        fallbacks=[Filters.regex('^Всё$')]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()