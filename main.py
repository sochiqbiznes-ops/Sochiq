import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers import start, clients, actions, report

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

start.register(dp)
clients.register(dp)
actions.register(dp)
report.register(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())