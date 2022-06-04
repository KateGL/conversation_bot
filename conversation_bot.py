# Учебный бот для демонстрации работы с ConversationHandler

from telegram.ext import Filters, MessageHandler, CommandHandler, ConversationHandler, Updater
from bot_factory import create_bot
from bot_engine_final import BotEngine
from const import BOT_SELECT_FOOD, BOT_SELECT_ADDRESS, BOT_DELIVERY, BOT_SELECT_CONTACTS



bot_engine = BotEngine()
conv_handler = ConversationHandler( # здесь строится логика разговора
    # точка входа в разговор
    entry_points=[CommandHandler('start', bot_engine.start,  pass_user_data=True)],
    # этапы разговора, каждый со своим списком обработчиков сообщений
    states={
        BOT_SELECT_CONTACTS: [MessageHandler(Filters.text & (~ Filters.command), bot_engine.get_contacts)],
        BOT_SELECT_FOOD: [MessageHandler(Filters.text & (~ Filters.command), bot_engine.select_food)],
        BOT_SELECT_ADDRESS: [MessageHandler(Filters.text & (~ Filters.command), bot_engine.select_address)],
        BOT_DELIVERY: [MessageHandler(Filters.text & (~ Filters.command), bot_engine.delivery)]
    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('exit', bot_engine.exit)],
)

updater = create_bot()
updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle()
