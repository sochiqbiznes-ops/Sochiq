from aiogram import Router, F
from aiogram.types import Message

from db import connect
from keyboards.barber_menu import barber_menu_kb

router = Router()

user_state = {}
current_barber = {}

@router.message(F.text == "➕ Mijoz qo‘shish")
async def add_client(message: Message):

    uid = message.from_user.id

    if uid not in current_barber:
        await message.answer("❌ Barber tanlanmagan")
        return

    user_state[uid] = "add_client"

    await message.answer("👤 Mijoz ismini yozing:")

@router.message()
async def save_client(message: Message):

    uid = message.from_user.id

    if uid not in user_state:
        return

    if user_state[uid] != "add_client":
        return

    barber_id = current_barber[uid]

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO clients (name, barber_id) VALUES (?, ?)",
        (message.text, barber_id)
    )

    conn.commit()
    conn.close()

    del user_state[uid]

    await message.answer("✅ Mijoz qo‘shildi")

@router.message(F.text == "👤 Mijozlar")
async def list_clients(message: Message):

    uid = message.from_user.id

    if uid not in current_barber:
        await message.answer("❌ Barber tanlanmagan")
        return

    barber_id = current_barber[uid]

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT name FROM clients WHERE barber_id = ?",
        (barber_id,)
    )

    clients = cur.fetchall()
    conn.close()

    text = "👤 Mijozlar:\n\n"

    if not clients:
        text += "❌ yo‘q"
    else:
        for c in clients:
            text += f"• {c[0]}\n"

    await message.answer(text)

