from aiogram import types
from database import *
from state import user_state
from utils.calc import calc

def register(dp):

    @dp.message()
    async def handler(m: types.Message):
        uid = m.from_user.id
        text = m.text

        state = user_state.get(uid, {})

        # ➕ ADD CLIENT
        if state.get("action") == "add":
            add_client(text)
            user_state[uid] = {}
            await m.answer("✔️ Qo‘shildi")
            return

        client = get_client(text)

        # 👤 OPEN CLIENT
        if client:
            name = client[1]
            price = client[2]
            taken = client[3]
            paid = client[4]

            total, debt = calc(client)

            user_state[uid] = {"client": name}

            kb = types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton("📦 Topshirish"), types.KeyboardButton("💳 To‘lov")],
                    [types.KeyboardButton("💰 Narx belgilash")]
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

        # 📦 TOPSHIRISH
        if text == "📦 Topshirish":
            user_state[uid]["action"] = "take"
            await m.answer("📦 Nechta dona?")
            return

        # 💳 TO‘LOV
        if text == "💳 To‘lov":
            user_state[uid]["action"] = "pay"
            await m.answer("💰 To‘lov summasi:")
            return

        # 💰 NARX
        if text == "💰 Narx belgilash":
            user_state[uid]["action"] = "price"
            await m.answer("💰 1 dona narx:")
            return

        # 🔢 NUMBER
        if text.isdigit():
            action = state.get("action")
            client = state.get("client")

            if not client:
                return

            value = int(text)

            if action == "take":
                update_field(client, "taken", value)
                await m.answer("✔️ Topshirildi")

            elif action == "pay":
                update_field(client, "paid", value)
                await m.answer("✔️ To‘lov")

            elif action == "price":
                set_field(client, "price", value)
                await m.answer("✔️ Narx")

            user_state[uid] = {}