from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from db import connect
from services.balance import calc_balance

router = Router()

state = {}


# =========================
# OPEN CLIENT → REPORT
# =========================
@router.callback_query(F.data.startswith("client:"))
async def open_client(call: CallbackQuery):
    client = call.data.split(":")[1]

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT received, paid, price 
        FROM clients 
        WHERE name = ?
    """, (client,))

    row = cur.fetchone()
    conn.close()

    if not row:
        await call.message.answer("❌ Mijoz topilmadi")
        return

    received, paid, price = row

    res = calc_balance(received, paid, price)

    await call.message.answer(
        f"""👤 {client}

📦 Olgan: {received}
💰 To‘langan (pul): {paid}
📊 Balans: {res['balance_money']} so‘m
"""
    )

    await call.answer()


# =========================
# TOPSHIRISH START
# =========================
@router.callback_query(F.data.startswith("give:"))
async def give_start(call: CallbackQuery):
    client = call.data.split(":")[1]

    state[call.from_user.id] = {
        "type": "give",
        "client": client
    }

    await call.message.answer("📦 Nechta dona berildi?")
    await call.answer()


# =========================
# TO‘LOV START
# =========================
@router.callback_query(F.data.startswith("pay:"))
async def pay_start(call: CallbackQuery):
    client = call.data.split(":")[1]

    state[call.from_user.id] = {
        "type": "pay",
        "client": client
    }

    await call.message.answer("💰 Summani kiriting:")
    await call.answer()


# =========================
# INPUT HANDLER
# =========================
@router.message()
async def input_handler(message: Message):
    uid = message.from_user.id

    if uid not in state:
        return

    data = state[uid]
    client = data["client"]

    conn = connect()
    cur = conn.cursor()

    # -------------------------
    # GIVE (DONA)
    # -------------------------
    if data["type"] == "give":
        qty = int(message.text)

        cur.execute("""
            UPDATE clients 
            SET received = received + ?
            WHERE name = ?
        """, (qty, client))

        conn.commit()
        conn.close()

        state.pop(uid)

        await message.answer("✅ Topshirildi")
        return

    # -------------------------
    # PAYMENT (PUL)
    # -------------------------
    if data["type"] == "pay":
        amount = int(message.text)

        cur.execute("""
            UPDATE clients 
            SET paid = paid + ?
            WHERE name = ?
        """, (amount, client))

        conn.commit()
        conn.close()

        state.pop(uid)

        await message.answer("✅ To‘lov qabul qilindi")
        return