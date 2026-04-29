from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def barber_inline_kb(barbers):
    buttons = []

    for b in barbers:
        buttons.append([
            InlineKeyboardButton(
                text=f"🏪 {b[1]}",
                callback_data=f"barber_{b[0]}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)