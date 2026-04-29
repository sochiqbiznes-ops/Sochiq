from aiogram import types
from database import add_client, get_clients
from state import user_state

def register(dp):

    @dp.message(lambda m: m.text == "➕ Mijoz qo‘shish")
    async def add(m: types.Message):
        user_state[m.from_user.id] = {"action": "add"}
        await m.answer("👤 Mijoz ismini yozing:")

    @dp.message(lambda m: m.text == "👥 Mijozlar")
    async def list_clients(m: types.Message):
        rows = get_clients()

        kb = types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=r[0])] for r in rows],
            resize_keyboard=True
        )

        await m.answer("👤 Mijoz tanlang:", reply_markup=kb)