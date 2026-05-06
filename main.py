import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db import init_db

from handlers import start, admin

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# routerlarni ulaymiz
dp.include_router(start.router)
dp.include_router(admin.router)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())