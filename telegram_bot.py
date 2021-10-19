from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, replymarkup
import logging
from environs import Env
import random
from parse_quiz import parse_quiz_file

env = Env()
env.read_env()

TELEGRAM_TOKEN = env('TELEGRAM_API_TOKEN')
CHAT_ID = env.int('CHAT_ID')

QUIZ_CONTENT = parse_quiz_file()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=CHAT_ID, reply_markup=reply_markup)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def send_question(bot, update):
    """Send to the user question."""

    if update.message.text == 'Новый вопрос':
        question = random.choice(list(QUIZ_CONTENT.keys()))
        update.message.reply_text(question)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, send_question))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()