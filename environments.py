from environs import Env

env = Env()
env.read_env()

TELEGRAM_TOKEN = env.str('TELEGRAM_API_TOKEN')
CHAT_ID = env.int('CHAT_ID')
REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT')
REDIS_PASSWORD = env.str('REDIS_PASSWORD')
VK_TOKEN = env.str('VK_API_TOKEN')