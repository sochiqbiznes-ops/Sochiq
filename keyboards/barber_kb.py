from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def barber_list_kb(barbers: list):
    buttons = []

    for b in barbers:
        buttons.append([
            InlineKeyboardButton(text=f"🏪 {b}", callback_data=f"barber:{b}")
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)