import asyncio
import os

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, ADMIN_ID
from db import init_db

# HANDLERS
from handlers import admin
from handlers import barber
from handlers import client


# =========================
# BOT INIT
# =========================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# INCLUDE ROUTERS
# =========================
dp.include_router(admin.router)
dp.include_router(barber.router)
dp.include_router(client.router)


# =========================
# ADMIN FILTER (GLOBAL SIMPLE CHECK)
# =========================
@dp.message()
async def global_block(message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Ruxsat yo‘q")


# =========================
# START BOT
# =========================
async def main():
    await init_db()
    print("🚀 Bot ishga tushdi...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())