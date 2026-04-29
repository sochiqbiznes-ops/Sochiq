from aiogram import types
from database import get_clients

def register(dp):

    @dp.message(commands=["start"])
    async def start(m: types.Message):
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="➕ Mijoz qo‘shish"), types.KeyboardButton(text="👥 Mijozlar")],
                [types.KeyboardButton(text="📊 Hisobot")]
            ],
            resize_keyboard=True
        )
        await m.answer("💼 CRM ishga tushdi", reply_markup=kb)