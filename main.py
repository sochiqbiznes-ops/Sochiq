import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =========================
# DATABASE (TEMP MEMORY)
# =========================
barbers = {}   # {name: [clients]}
clients = {}   # {name: {received, paid, price, barber}}

state = {}     # simple state storage


# =========================
# KEYBOARDS
# =========================
def barber_list_kb():
    kb = []
    for b in barbers.keys():
        kb.append([InlineKeyboardButton(text=b, callback_data=f"barber:{b}")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def client_list_kb(barber):
    kb = []
    for c in barbers[barber]:
        kb.append([InlineKeyboardButton(text=c, callback_data=f"client:{c}")])
    kb.append([InlineKeyboardButton(text="➕ Mijoz qo‘shish", callback_data=f"addclient:{barber}")])
    kb.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back:home")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def client_menu_kb(client):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Topshirish", callback_data=f"give:{client}")],
        [InlineKeyboardButton(text="💰 To‘lov", callback_data=f"pay:{client}")],
        [InlineKeyboardButton(text="📊 Hisobot", callback_data=f"report:{client}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back:barber")]
    ])


# =========================
# START
# =========================
@dp.message(CommandStart())
async def start(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "🏠 ADMIN PANEL",
            reply_markup=barber_list_kb()
        )
    else:
        await message.answer(
            "🏪 Sartaroshxonalar:",
            reply_markup=barber_list_kb()
        )


# =========================
# CALLBACK HANDLER
# =========================
@dp.callback_query()
async def cb_handler(call: CallbackQuery):
    data = call.data

    # -------------------------
    # BARBER OPEN
    # -------------------------
    if data.startswith("barber:"):
        barber = data.split(":")[1]

        await call.message.edit_text(
            f"🏪 {barber}",
            reply_markup=client_list_kb(barber)
        )

    # -------------------------
    # ADD CLIENT START
    # -------------------------
    elif data.startswith("addclient:"):
        barber = data.split(":")[1]
        state[call.from_user.id] = {"addclient": barber}

        await call.message.answer("👤 Mijoz ismini yozing:")

    # -------------------------
    # CLIENT OPEN
    # -------------------------
    elif data.startswith("client:"):
        client = data.split(":")[1]

        c = clients.get(client, {"received": 0, "paid": 0, "price": 2000})

        balance = (c["paid"] // c["price"]) - c["received"]

        text = f"""👤 {client}

📦 Olgan: {c['received']}
💰 To‘lagan (dona): {c['paid']//c['price']}
📊 Balans: {balance * c['price']} so‘m
"""

        await call.message.edit_text(
            text,
            reply_markup=client_menu_kb(client)
        )

    # -------------------------
    # TOPSHIRISH
    # -------------------------
    elif data.startswith("give:"):
        client = data.split(":")[1]
        state[call.from_user.id] = {"give": client}
        await call.message.answer("📦 Nechta dona berildi?")

    # -------------------------
    # TO‘LOV
    # -------------------------
    elif data.startswith("pay:"):
        client = data.split(":")[1]
        state[call.from_user.id] = {"pay": client}
        await call.message.answer("💰 Summani kiriting:")

    # -------------------------
    # REPORT
    # -------------------------
    elif data.startswith("report:"):
        client = data.split(":")[1]
        c = clients.get(client, {"received": 0, "paid": 0, "price": 2000})

        balance = (c["paid"] // c["price"]) - c["received"]

        await call.message.answer(
            f"""📊 HISOBOT

👤 {client}
📦 Olgan: {c['received']}
💰 To‘langan: {c['paid']}
📊 Balans: {balance * c['price']} so‘m"""
        )

    await call.answer()


# =========================
# TEXT HANDLER (INPUTS)
# =========================
@dp.message()
async def text_handler(message: Message):
    uid = message.from_user.id

    # -------------------------
    # ADD CLIENT
    # -------------------------
    if uid in state and "addclient" in state[uid]:
        barber = state[uid]["addclient"]

        name = message.text

        if barber not in barbers:
            barbers[barber] = []

        barbers[barber].append(name)

        clients[name] = {
            "received": 0,
            "paid": 0,
            "price": 2000,
            "barber": barber
        }

        del state[uid]

        await message.answer("✅ Mijoz qo‘shildi")
        return

    # -------------------------
    # TOPSHIRISH
    # -------------------------
    if uid in state and "give" in state[uid]:
        client = state[uid]["give"]
        qty = int(message.text)

        clients[client]["received"] += qty

        del state[uid]

        await message.answer("✅ Topshirildi")
        return

    # -------------------------
    # TO‘LOV
    # -------------------------
    if uid in state and "pay" in state[uid]:
        client = state[uid]["pay"]
        amount = int(message.text)

        price = clients[client]["price"]
        clients[client]["paid"] += amount

        del state[uid]

        await message.answer("✅ To‘lov qabul qilindi")
        return


# =========================
# RUN
# =========================
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())