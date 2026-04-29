from aiogram import types
from database import *
from state import user_state

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
            name, price, taken, paid = client[1], client[2], client[3], client[4]

            kb = types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton("📦 Topshirish"), types.KeyboardButton("💳 To‘lov")],
                    [types.KeyboardButton("💰 Narx")]
                ],
                resize_keyboard=True
            )

            user_state[uid] = {"client": name}

            await m.answer(f"""
👤 {name}

📦 Olingan: {taken}
💰 Narx: {price}
💳 To‘langan: {paid}
""", reply_markup=kb)
            return

        # 📦 TOPSHIRISH
        if text == "📦 Topshirish":
            user_state[uid]["action"] = "take"
            await m.answer("Nechta dona?")
            return

        # 💳 TO‘LOV
        if text == "💳 To‘lov":
            user_state[uid]["action"] = "pay"
            await m.answer("To‘lov summasi:")
            return

        # 💰 NARX
        if text == "💰 Narx":
            user_state[uid]["action"] = "price"
            await m.answer("1 dona narx:")
            return

        # NUMBER
        if text.isdigit():
            action = state.get("action")
            client = state.get("client")

            if not client:
                return

            if action == "take":
                update(client, "taken", int(text))
                await m.answer("✔️ Qo‘shildi")

            elif action == "pay":
                update(client, "paid", int(text))
                await m.answer("✔️ To‘lov")

            elif action == "price":
                set_value(client, "price", int(text))
                await m.answer("✔️ Narx")

            user_state[uid] = {}