from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from db import connect
from keyboards.main_menu import barber_inline_kb
from keyboards.reply_menu import admin_reply_kb

router = Router()

user_state = {}
current_barber = {}


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

@router.message(F.text == "➕ Sartaroshxona qo‘shish")
async def add_barber(message: Message):

    user_state[message.from_user.id] = "add_barber"

    await message.answer("🏪 Sartaroshxona nomini yozing:")


@router.message()
async def save_text(message: Message):

    uid = message.from_user.id

    if uid not in user_state:
        return

    state = user_state[uid]

    conn = connect()
    cur = conn.cursor()

    if state == "add_barber":
        cur.execute(
            "INSERT INTO barbers (name) VALUES (?)",
            (message.text,)
        )
        conn.commit()

        del user_state[uid]

        cur.execute("SELECT * FROM barbers")
        barbers = cur.fetchall()

        conn.close()

        await message.answer("✅ Qo‘shildi")

        await message.answer(
            "🏪 Yangilangan ro‘yxat:",
            reply_markup=barber_inline_kb(barbers)
        )

@router.callback_query(F.data.startswith("barber_"))
async def open_barber(call: CallbackQuery):

    barber_id = int(call.data.split("_")[1])

    current_barber[call.from_user.id] = barber_id

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT name FROM barbers WHERE id = ?", (barber_id,))
    barber = cur.fetchone()

    conn.close()

    await call.message.answer(
        f"🏪 {barber[0]} ichiga kirdingiz\n\n"
        "👉 Keyingi bosqich: mijoz system",
    )

    await call.answer()