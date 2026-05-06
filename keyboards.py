from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Qarz qo‘shish")],
            [KeyboardButton(text="📊 Qarzlar")]
        ],
        resize_keyboard=True
    )