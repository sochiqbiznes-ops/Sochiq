import os
import sqlite3
from aiogram import Bot, Dispatcher, types, executor

# =====================
# 🔐 ENV
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

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
# 🧠 STATE (TEMP)
# =====================
user_state = {}  # {user_id: {"action": "", "client": ""}}

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
    cur.execute(f"UPDATE clients SET {field} = ? WHERE name=?", (value, name))
    conn.commit()

def calc(client):
    total = client[2] * client[3]
    debt = total - client[4]
    return total, debt

# =====================
# 🏠 START
# =====================
@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("➕ Mijoz qo‘shish", "👥 Mijozlar")
    kb.add("📊 Hisobot")
    await m.answer("💼 CRM tizim ishga tushdi", reply_markup=kb)

# =====================
# ➕ ADD CLIENT
# =====================
@dp.message_handler(lambda m: m.text == "➕ Mijoz qo‘shish")
async def add(m: types.Message):
    user_state[m.from_user.id] = {"action": "add_client"}
    await m.answer("👤 Mijoz ismini yozing:")

# =====================
# 👥 LIST CLIENTS
# =====================
@dp.message_handler(lambda m: m.text == "👥 Mijozlar")
async def list_clients(m: types.Message):
    cur.execute("SELECT name FROM clients")
    rows = cur.fetchall()

    if not rows:
        await m.answer("❌ Mijoz yo‘q")
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for r in rows:
        kb.add(r[0])

    await m.answer("👤 Mijoz tanlang:", reply_markup=kb)

# =====================
# MAIN HANDLER
# =====================
@dp.message_handler()
async def handler(m: types.Message):
    uid = m.from_user.id
    text = m.text

    state = user_state.get(uid, {})

    # ➕ CREATE CLIENT
    if state.get("action") == "add_client":
        try:
            cur.execute("INSERT INTO clients (name) VALUES (?)", (text,))
            conn.commit()
            await m.answer(f"✔️ {text} qo‘shildi")
        except:
            await m.answer("❌ Bunday mijoz bor")
        user_state[uid] = {}
        return

    client = get_client(text)

    # 👤 OPEN CLIENT PROFILE
    if client:
        name = client[1]
        price = client[2]
        taken = client[3]
        paid = client[4]

        total, debt = calc(client)

        user_state[uid] = {"client": name}

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add("📦 Topshirish", "💳 To‘lov")
        kb.add("💰 Narx")

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
        await m.answer("💰 To‘lov summasi (so‘m):")
        return

    # =====================
    # 💰 NARX
    # =====================
    if text == "💰 Narx":
        user_state[uid]["action"] = "price"
        await m.answer("💰 1 dona narxini kiriting:")
        return

    # =====================
    # NUMBERS INPUT
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
# 📊 HISOBOT
# =====================
@dp.message_handler(lambda m: m.text == "📊 Hisobot")
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
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)