import asyncio
import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db import init_db
from handlers.admin import router as admin_router

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(admin_router)


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())