import os
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# =====================
# 🔐 ENV
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =====================
# 🗄 DATABASE
# =====================
conn = sqlite3.connect("crm.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price INTEGER DEFAULT 0,
    taken INTEGER DEFAULT 0,
    paid INTEGER DEFAULT 0
)
""")
conn.commit()

# =====================
# 🧠 STATE
# =====================
user_state = {}

# =====================
# HELPERS
# =====================
def get_client(name):
    cur.execute("SELECT * FROM clients WHERE name=?", (name,))
    return cur.fetchone()

def update(name, field, value):
    cur.execute(f"UPDATE clients SET {field} = {field} + ? WHERE name=?", (value, name))
    conn.commit()

def set_value(name, field, value):
    cur.execute(f"UPDATE clients SET {field}=? WHERE name=?", (value, name))
    conn.commit()

def calc(c):
    total = c[2] * c[3]
    debt = total - c[4]
    return total, debt

# =====================
# 🏠 START
# =====================
@dp.message(CommandStart())
async def start(m: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="➕ Mijoz qo‘shish"), types.KeyboardButton(text="👥 Mijozlar")],
            [types.KeyboardButton(text="📊 Hisobot")]
        ],
        resize_keyboard=True
    )

    await m.answer("💼 CRM tizim ishga tushdi", reply_markup=kb)

# =====================
# ➕ ADD CLIENT
# =====================
@dp.message(F.text == "➕ Mijoz qo‘shish")
async def add_client(m: types.Message):
    user_state[m.from_user.id] = {"action": "add"}
    await m.answer("👤 Mijoz ismini yozing:")

# =====================
# 👥 LIST CLIENTS
# =====================
@dp.message(F.text == "👥 Mijozlar")
async def clients(m: types.Message):
    cur.execute("SELECT name FROM clients")
    rows = cur.fetchall()

    if not rows:
        await m.answer("❌ Mijoz yo‘q")
        return

    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=r[0])] for r in rows],
        resize_keyboard=True
    )

    await m.answer("👤 Mijoz tanlang:", reply_markup=kb)

# =====================
# MAIN HANDLER
# =====================
@dp.message()
async def handler(m: types.Message):
    uid = m.from_user.id
    text = m.text

    state = user_state.get(uid, {})

    # ➕ ADD CLIENT SAVE
    if state.get("action") == "add":
        try:
            cur.execute("INSERT INTO clients (name) VALUES (?)", (text,))
            conn.commit()
            await m.answer("✔️ Qo‘shildi")
        except:
            await m.answer("❌ Bunday mijoz bor")

        user_state[uid] = {}
        return

    # 👤 OPEN CLIENT
    client = get_client(text)

    if client:
        name, price, taken, paid = client[1], client[2], client[3], client[4]
        total, debt = calc(client)

        user_state[uid] = {"client": name}

        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="📦 Topshirish"), types.KeyboardButton(text="💳 To‘lov")],
                [types.KeyboardButton(text="💰 Narx")]
            ],
            resize_keyboard=True
        )

        await m.answer(f"""
👤 {name}

📦 Olingan: {taken}
💰 Narx: {price}

💳 To‘langan: {paid}
❌ Qarz: {debt}
""", reply_markup=kb)
        return

    # =====================
    # 📦 TOPSHIRISH
    # =====================
    if text == "📦 Topshirish":
        user_state[uid]["action"] = "take"
        await m.answer("📦 Nechta dona berildi?")
        return

    # =====================
    # 💳 TO‘LOV
    # =====================
    if text == "💳 To‘lov":
        user_state[uid]["action"] = "pay"
        await m.answer("💰 To‘lov summasi:")
        return

    # =====================
    # 💰 NARX
    # =====================
    if text == "💰 Narx":
        user_state[uid]["action"] = "price"
        await m.answer("💰 1 dona narxini kiriting:")
        return

    # =====================
    # NUMBER INPUT
    # =====================
    if text.isdigit():
        action = state.get("action")
        client = state.get("client")

        if not client:
            return

        if action == "take":
            update(client, "taken", int(text))
            await m.answer("✔️ Topshirildi")

        elif action == "pay":
            update(client, "paid", int(text))
            await m.answer("✔️ To‘lov qabul qilindi")

        elif action == "price":
            set_value(client, "price", int(text))
            await m.answer("✔️ Narx saqlandi")

        user_state[uid] = {}
        return

# =====================
# 📊 REPORT
# =====================
@dp.message(F.text == "📊 Hisobot")
async def report(m: types.Message):
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()

    total_debt = 0

    for r in rows:
        total = r[2] * r[3]
        debt = total - r[4]
        total_debt += debt

    await m.answer(f"📊 Umumiy qarz: {total_debt} so‘m")

# =====================
# RUN
# =====================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())