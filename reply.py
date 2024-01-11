from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_buttons():
    btn1 = KeyboardButton(text='💰 My balance')
    btn2 = KeyboardButton(text='💸 Withdraw')
    btn3 = KeyboardButton(text='🔗 Rental link')
    btn4 = KeyboardButton(text='Bot info')
    design = [
        [btn1, btn2],
        [btn3, btn4]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
