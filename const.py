from telegram import ReplyKeyboardMarkup

BOT_SELECT_CONTACTS, BOT_SELECT_FOOD, BOT_SELECT_ADDRESS, BOT_DELIVERY  = range(4)
FOOD = ['Пицца', 'Роллы', 'Суп', 'Торт']
ANSWER_YES = 'ДА'
ANSWER_NO = 'НЕТ'
ANSWERS = [ANSWER_YES, ANSWER_NO]

FINISH_BUTTONS = ReplyKeyboardMarkup([ ['/start'] ])
ALWAYS_SHOW_BUTTON_CAPTIONS = ['/exit']

FOOD_BUTTONS = ReplyKeyboardMarkup([
                FOOD,
                ALWAYS_SHOW_BUTTON_CAPTIONS
            ])