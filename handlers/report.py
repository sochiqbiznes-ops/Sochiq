from aiogram import types
from database import get_client

def register(dp):

    @dp.message(lambda m: m.text == "📊 Hisobot")
    async def report(m: types.Message):
        await m.answer("Hisobot modul keyin qo‘shiladi ✔️")