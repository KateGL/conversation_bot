
import logging
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
from const import *
from utils import get_chat_info

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)



class BotEngine():
    
    def start(self, update, context):
        chat = get_chat_info(update)
        if not context.user_data.get("contacts"):
            context.user_data["contacts"] = update.message.chat.first_name

        context.bot.send_message(chat_id=chat.id, text=f'Привет, {context.user_data["contacts"]}!')

        if context.user_data["contacts"] == update.message.chat.first_name:
            context.bot.send_message(chat_id=chat.id, text='Напиши как тебя называть')
            return BOT_SELECT_CONTACTS

        if context.user_data.get("food"):
            buttons = ReplyKeyboardMarkup([
                [ANSWER_YES, ANSWER_NO],
                ALWAYS_SHOW_BUTTON_CAPTIONS
            ])
            context.bot.send_message(
               chat_id=chat.id, 
               text=f'В прошлый раз ты заказывал, {context.user_data.get("food")}! \n Повторить?',
               reply_markup=buttons
               ) 
            return BOT_SELECT_FOOD
       
        context.bot.send_message(chat_id=chat.id, 
                                    text=f'{context.user_data["contacts"]}, Выбери что ты хочешь заказать ',
                                    reply_markup=FOOD_BUTTONS
                                    )
        return BOT_SELECT_FOOD

    def get_contacts(self, update, context):
        chat = get_chat_info(update)
        context.user_data["contacts"] = update.message.text    
        context.bot.send_message(chat_id=chat.id, 
                                    text=f'{context.user_data["contacts"]}, Выбери что ты хочешь заказать ',
                                    reply_markup=FOOD_BUTTONS
                                    )
        return BOT_SELECT_FOOD

    def exit(self, update, context):
        chat = get_chat_info(update)
        context.bot.send_message(
            chat_id=chat.id, 
            text=f'До свидания, {context.user_data["contacts"]}!',
            reply_markup=FINISH_BUTTONS
            )
        return ConversationHandler.END

    def select_food(self, update, context):
        chat = get_chat_info(update)

        if update.message.text not in FOOD + ANSWERS:
            context.bot.send_message(chat_id=chat.id, 
                                    text=f'{context.user_data["contacts"]}, я не знаю такого продукта. \n'
                                     'Пожалуйста, выбери из списка на кнопках'
                                    )
            return BOT_SELECT_FOOD

        if update.message.text == ANSWER_NO:
            buttons = ReplyKeyboardMarkup([
                FOOD,
                ALWAYS_SHOW_BUTTON_CAPTIONS
            ])

            context.bot.send_message(chat_id=chat.id, 
                                    text='Выбери что ты хочешь заказать',
                                    reply_markup=buttons
                                    )
            return BOT_SELECT_FOOD

        if update.message.text != ANSWER_YES:
            context.user_data["food"] = update.message.text 

        buttons = ReplyKeyboardMarkup([
                ['Все ок, доставьте заказ'],
                ALWAYS_SHOW_BUTTON_CAPTIONS
            ])
        context.bot.send_message(chat_id=chat.id, 
                                    text=f'Ты заказываешь {context.user_data["food"]}',
                                    reply_markup=buttons
                                    )      
        return BOT_SELECT_ADDRESS

    def select_address(self, update, context):
        selections = []
        if context.user_data.get("address"):
            selections.append(context.user_data["address"])

        buttons = ReplyKeyboardMarkup([
                selections,
                ALWAYS_SHOW_BUTTON_CAPTIONS
            ])
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, 
                                    text='Пожалуйста, введи адрес доставки',
                                    reply_markup=buttons
                                    )         
        return BOT_DELIVERY

    def delivery(self, update, context):
        context.user_data["address"] = update.message.text
        text = 'Спасибо за заказ! \n'+f'{context.user_data["contacts"]}, ожидайте {context.user_data["food"]} по адресу {context.user_data["address"]}'
        update.message.reply_text(text, reply_markup=FINISH_BUTTONS)
        return ConversationHandler.END
    