from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def client_menu_kb(client: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📦 Topshirish", callback_data=f"give:{client}")
        ],
        [
            InlineKeyboardButton(text="💰 To‘lov", callback_data=f"pay:{client}")
        ],
        [
            InlineKeyboardButton(text="📊 Hisobot", callback_data=f"report:{client}")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="back:clients")
        ]
    ])