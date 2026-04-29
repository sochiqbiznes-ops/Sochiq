from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from db import connect
from keyboards import main_menu_kb

router = Router()

user_state = {}


@router.message(F.text == "/start")
async def start_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Ruxsat yo‘q")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM barbers")
    barbers = cur.fetchall()
    conn.close()

    await message.answer(
        "🏠 Bosh menyu",
        reply_markup=main_menu_kb(barbers)
    )


@router.callback_query()
async def callback_handler(call: CallbackQuery):
    data = call.data

    if data == "add_barber":
        user_state[call.from_user.id] = "barber"
        await call.message.answer("🏪 Sartaroshxona nomini yozing:")

    elif data.startswith("barber_"):
        barber_id = int(data.split("_")[1])
        user_state[call.from_user.id] = f"client_{barber_id}"
        await call.message.answer("👤 Mijoz ismini yozing:")

    await call.answer()


@router.message()
async def text_handler(message: Message):
    uid = message.from_user.id

    if uid not in user_state:
        return

    state = user_state[uid]

    conn = connect()
    cur = conn.cursor()

    if state == "barber":
        cur.execute(
            "INSERT INTO barbers (name) VALUES (?)",
            (message.text,)
        )
        conn.commit()
        conn.close()

        del user_state[uid]
        await message.answer("✅ Sartaroshxona qo‘shildi")
        return

    if state.startswith("client_"):
        barber_id = int(state.split("_")[1])

        cur.execute(
            "INSERT INTO clients (name, barber_id) VALUES (?, ?)",
            (message.text, barber_id)
        )
        conn.commit()
        conn.close()

        del user_state[uid]
        await message.answer("✅ Mijoz qo‘shildi")