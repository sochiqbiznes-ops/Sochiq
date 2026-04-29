from aiogram import Router, F
from aiogram.types import Message

from db import connect
from keyboards.main_menu import barber_inline_kb
from keyboards.reply_menu import admin_reply_kb

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message):

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM barbers")
    barbers = cur.fetchall()

    conn.close()

    await message.answer(
        "🏠 Bosh menyu",
        reply_markup=admin_reply_kb()
    )

    await message.answer(
        "🏪 Sartaroshxonalar:",
        reply_markup=barber_inline_kb(barbers)
    )