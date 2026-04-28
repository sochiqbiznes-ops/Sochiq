from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def client_list_kb(clients: list, barber: str):
    buttons = []

    for c in clients:
        buttons.append([
            InlineKeyboardButton(text=f"👤 {c}", callback_data=f"client:{c}")
        ])

    buttons.append([
        InlineKeyboardButton(text="➕ Mijoz qo‘shish", callback_data=f"add_client:{barber}")
    ])

    buttons.append([
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back:barbers")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)