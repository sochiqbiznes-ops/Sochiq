from aiogram.filters import CommandStart
from aiogram import types

def register(dp):

    @dp.message(CommandStart())
    async def start(m: types.Message):
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton("➕ Mijoz qo‘shish"), types.KeyboardButton("👥 Mijozlar")],
                [types.KeyboardButton("📊 Hisobot")]
            ],
            resize_keyboard=True
        )

        await m.answer("💼 CRM ishga tushdi", reply_markup=kb)