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
            [types.KeyboardButton(text="➕ Mijoz qo‘shish")],
            [types.KeyboardButton(text="👥 Mijozlar")],
            [types.KeyboardButton(text="📊 Hisobot")]
        ],
        resize_keyboard=True
    )
    await m.answer("💼 CRM ishga tushdi", reply_markup=kb)

# ================= ADD =================
@dp.message(F.text == "➕ Mijoz qo‘shish")
async def add(m: types.Message):
    state[m.from_user.id] = {"action": "add"}
    await m.answer("👤 Ism yozing:")

# ================= LIST =================
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

    await m.answer("👤 Tanlang:", reply_markup=kb)

# ================= REPORT (YO‘QOLGAN JOY FIX) =================
@dp.message(F.text == "📊 Hisobot")
async def report(m: types.Message):
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()

    total_debt = 0

    for r in rows:
        price = r[2]
        taken = r[3]
        paid = r[4]

        total = price * taken
        debt = total - paid
        total_debt += debt

    await m.answer(f"📊 Jami qarz: {total_debt} so‘m")

# ================= CLIENT OPEN =================
@dp.message()
async def handler(m: types.Message):
    uid = m.from_user.id
    text = m.text
    st = state.get(uid, {})

    # ➕ ADD
    if st.get("action") == "add":
        cur.execute("INSERT OR IGNORE INTO clients (name) VALUES (?)", (text,))
        conn.commit()
        state[uid] = {}
        await m.answer("✔️ Qo‘shildi")
        return

    # 👤 OPEN CLIENT
    cur.execute("SELECT * FROM clients WHERE name=?", (text,))
    c = cur.fetchone()

    if c:
        state[uid] = {
            "client_id": c[0],
            "name": c[1]
        }

        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton("📦 Topshirish"), types.KeyboardButton("💳 To‘lov")],
                [types.KeyboardButton("💰 Narx")]
            ],
            resize_keyboard=True
        )

        await m.answer(f"""
👤 {c[1]}

📦 Olingan: {c[3]}
💰 Narx: {c[2]}
💳 To‘langan: {c[4]}
""", reply_markup=kb)
        return

    # ================= ACTION =================
    if text in ["📦 Topshirish", "💳 To‘lov", "💰 Narx"]:
        state[uid]["action"] = text
        await m.answer("Raqam kiriting:")
        return

    # ================= NUMBERS =================
    if text.isdigit():
        action = st.get("action")
        client_id = st.get("client_id")

        if not client_id:
            return

        val = int(text)

        if action == "📦 Topshirish":
            cur.execute("UPDATE clients SET taken = taken + ? WHERE id=?", (val, client_id))

        elif action == "💳 To‘lov":
            cur.execute("UPDATE clients SET paid = paid + ? WHERE id=?", (val, client_id))

        elif action == "💰 Narx":
            cur.execute("UPDATE clients SET price=? WHERE id=?", (val, client_id))

        conn.commit()
        state[uid] = {}

        await m.answer("✔️ Saqlandi")

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())