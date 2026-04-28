import os
import logging

from aiogram import Bot, Dispatcher, executor, types

# ENV VARIABLES
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# TOKEN tekshiruv (eng muhim joy)
if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Railway Environment Variables ni tekshir.")

# Bot va dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# logging
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Salom 👋 Bot ishlayapti!")


@dp.message_handler(commands=['id'])
async def get_id(message: types.Message):
    await message.answer(f"Sizning ID: {message.from_user.id}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)