from telegram.ext import Updater

def create_bot() -> Updater:
    BOT_TOKEN = 'добавьте токен своего бота'
    # или используете переменные окружения
    return Updater(token=BOT_TOKEN)
