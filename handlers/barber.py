from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from db import connect
from keyboards.client_kb import client_list_kb

router = Router()

state = {}


# =========================
# OPEN BARBER → CLIENT LIST
# =========================
@router.callback_query(F.data.startswith("barber:"))
async def open_barber(call: CallbackQuery):
    barber = call.data.split(":")[1]

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT name FROM clients WHERE barber = ?", (barber,))
    rows = cur.fetchall()
    conn.close()

    clients = [r[0] for r in rows]

    await call.message.answer(
        f"🏪 {barber}\n👤 Mijozlar:",
        reply_markup=client_list_kb(clients, barber)
    )

    await call.answer()


# =========================
# ADD CLIENT START
# =========================
@router.callback_query(F.data.startswith("add_client:"))
async def add_client_start(call: CallbackQuery):
    barber = call.data.split(":")[1]

    state[call.from_user.id] = {"barber": barber}

    await call.message.answer("👤 Mijoz ismini yozing:")

    await call.answer()


# =========================
# SAVE CLIENT
# =========================
@router.message()
async def save_client(message: Message):
    uid = message.from_user.id

    if uid not in state:
        return

    if "barber" not in state[uid]:
        return

    barber = state[uid]["barber"]
    name = message.text

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO clients (name, barber) VALUES (?, ?)",
        (name, barber)
    )

    conn.commit()
    conn.close()

    state.pop(uid)

    await message.answer(f"✅ Mijoz qo‘shildi: {name}")


# =========================
# BACK SYSTEM (BASIC)
# =========================
@router.callback_query(F.data == "back:barbers")
async def back_to_barbers(call: CallbackQuery):
    await call.message.answer("🔙 Orqaga...")
    await call.answer()