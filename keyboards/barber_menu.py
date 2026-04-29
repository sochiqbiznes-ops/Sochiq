from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def barber_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Mijoz qo‘shish")],
            [KeyboardButton(text="🗑 Mijoz o‘chirish")],
            [KeyboardButton(text="📊 Hisobot")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True
    )