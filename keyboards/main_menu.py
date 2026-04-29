from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def barber_inline_kb(barbers):
    buttons = []

    for barber in barbers:
        buttons.append([
            InlineKeyboardButton(
                text=f"🏪 {barber[1]}",
                callback_data=f"barber_{barber[0]}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)