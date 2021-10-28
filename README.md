## Table of content

- [About the project](#about-the-project)
- [Installation](#installation)
- [How to run](#how-to-run)


## About the project

This is a chatbot for quizzes. It works on two platforms at once: Telegram and Vkontakte

Telegram: @acostyle_quiz_bot
VK: [@acostyle_quiz](https://vk.com/club207142712)


## Installation

* Install [Poetry](https://python-poetry.org/) and make;
* Clone github repository:
```bash
git clone https://github.com/acostyle/quiz_bot
```
* Go to folder with project:
```bash
cd quiz_bot
```
* Install dependencies:
```bash
make install
```
* Create a bot in Telegram via [BotFather](https://t.me/BotFather), and get it API token;
* Find out your chat id in the [@userinfobot](https://t.me/userinfobot)
* Create a .env.dev file with the following content:
```.env
TELEGRAM_API_TOKEN='telegram token'
CHAT_ID=chat ID
REDIS_HOST='redis endpoint'
REDIS_PORT=redis port
REDIS_PASSWORD='redis password'
VK_API_TOKEN='vk token'
```


## How to run

Run Telegram bot:
```bash
python telegram_bot.py
```

Run VK bot:
```bash
python vk_bot.py
```
