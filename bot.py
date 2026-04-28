import os
from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Bot ishladi ✅")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)