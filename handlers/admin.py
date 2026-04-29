from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from db import connect
from keyboards.main_menu import barber_inline_kb
from keyboards.reply_menu import admin_reply_kb

router = Router()
user_state = {}


# =====================
# START
# =====================
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
        reply_markup=admin_reply_kb()
    )

    await message.answer(
        "🏪 Sartaroshxonalar:",
        reply_markup=barber_inline_kb(barbers)
    )


# =====================
# REPLY BUTTON
# =====================
@router.message(F.text == "➕ Sartaroshxona qo‘shish")
async def add_barber_button(message: Message):
    user_state[message.from_user.id] = "barber"
    await message.answer("🏪 Sartaroshxona nomini yozing:")


# =====================
# INLINE BARBER
# =====================
@router.callback_query(F.data.startswith("barber_"))
async def open_barber(call: CallbackQuery):
    barber_id = int(call.data.split("_")[1])

    user_state[call.from_user.id] = f"client_{barber_id}"

    await call.message.answer("👤 Mijoz ismini yozing:")
    await call.answer()


# =====================
# TEXT SAVE
# =====================
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