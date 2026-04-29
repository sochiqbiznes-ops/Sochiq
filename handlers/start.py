from aiogram import types
from aiogram.filters import CommandStart

def register(dp):

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