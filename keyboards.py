from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb(barbers):
    buttons = []

    for barber in barbers:
        buttons.append([
            InlineKeyboardButton(
                text=f"🏪 {barber[1]}",
                callback_data=f"barber_{barber[0]}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="➕ Sartaroshxona qo‘shish",
            callback_data="add_barber"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)