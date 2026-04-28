from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.barber_kb import barber_list_kb
from db import connect

router = Router()

# =========================
# TEMP MEMORY (simple)
# =========================
barbers_cache = []
add_state = {}


# =========================
# START ADMIN PANEL
# =========================
@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT name FROM barbers")
    rows = cur.fetchall()
    conn.close()

    global barbers_cache
    barbers_cache = [r[0] for r in rows]

    await message.answer(
        "🏠 ADMIN PANEL",
        reply_markup=barber_list_kb(barbers_cache)
    )


# =========================
# ADD BARBER START
# =========================
@router.message(F.text == "➕ Sartaroshxona qo‘shish")
async def add_barber_start(message: Message):
    add_state["waiting"] = True
    await message.answer("🏪 Sartaroshxona nomini yozing:")


# =========================
# SAVE BARBER
# =========================
@router.message()
async def save_barber(message: Message):
    if not add_state.get("waiting"):
        return

    name = message.text

    conn = connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO barbers (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    add_state["waiting"] = False

    await message.answer(f"✅ Qo‘shildi: {name}")


# =========================
# BARBER OPEN (INLINE)
# =========================
@router.callback_query(F.data.startswith("barber:"))
async def open_barber(call: CallbackQuery):
    barber = call.data.split(":")[1]

    await call.message.answer(
        f"🏪 {barber}\n\n"
        "➕ Mijoz qo‘shish\n"
        "📊 Hisobot\n"
        "🔙 Orqaga"
    )

    await call.answer()