import os
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================= DB =================
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

state = {}

# ================= START =================
@dp.message(CommandStart())
async def start(m: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="➕ Mijoz qo‘shish"), types.KeyboardButton(text="👥 Mijozlar")],
            [types.KeyboardButton(text="📊 Hisobot")]
        ],
        resize_keyboard=True
    )
    await m.answer("💼 CRM ishga tushdi", reply_markup=kb)

# ================= ADD CLIENT =================
@dp.message(F.text == "➕ Mijoz qo‘shish")
async def add(m: types.Message):
    state[m.from_user.id] = {"action": "add"}
    await m.answer("👤 Mijoz ismini yozing:")

# ================= LIST =================
@dp.message(F.text == "👥 Mijozlar")
async def list_clients(m: types.Message):
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

# ================= MAIN =================
@dp.message()
async def handler(m: types.Message):
    uid = m.from_user.id
    text = m.text

    st = state.get(uid, {})

    # ADD
    if st.get("action") == "add":
        cur.execute("INSERT OR IGNORE INTO clients (name) VALUES (?)", (text,))
        conn.commit()
        state[uid] = {}
        await m.answer("✔️ Qo‘shildi")
        return

    # OPEN CLIENT
    cur.execute("SELECT * FROM clients WHERE name=?", (text,))
    c = cur.fetchone()

    if c:
        name = c[1]
        price = c[2]
        taken = c[3]
        paid = c[4]

        state[uid] = {"client": name}

        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton("📦 Topshirish"), types.KeyboardButton("💳 To‘lov")],
                [types.KeyboardButton("💰 Narx")]
            ],
            resize_keyboard=True
        )

        await m.answer(f"""
👤 {name}

📦 {taken}
💰 {price}
💳 {paid}
""", reply_markup=kb)
        return

    # ACTIONS
    if text in ["📦 Topshirish", "💳 To‘lov", "💰 Narx"]:
        state[uid]["action"] = text
        await m.answer("Raqam kiriting:")
        return

    # NUMBERS
    if text.isdigit():
        action = st.get("action")
        client = st.get("client")

        if not client:
            return

        val = int(text)

        if action == "📦 Topshirish":
            cur.execute("UPDATE clients SET taken = taken + ? WHERE name=?", (val, client))

        elif action == "💳 To‘lov":
            cur.execute("UPDATE clients SET paid = paid + ? WHERE name=?", (val, client))

        elif action == "💰 Narx":
            cur.execute("UPDATE clients SET price=? WHERE name=?", (val, client))

        conn.commit()
        state[uid] = {}
        await m.answer("✔️ Saqlandi")

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())