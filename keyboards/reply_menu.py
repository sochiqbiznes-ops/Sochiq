from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_reply_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Sartaroshxona qo‘shish")],
            [KeyboardButton(text="🗑 Sartaroshxona o‘chirish")],
            [KeyboardButton(text="📊 Umumiy hisobot")]
        ],
        resize_keyboard=True
    )