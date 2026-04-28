from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import add_client

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("➕ Mijoz qo‘shish"))


class AddClientState(StatesGroup):
    waiting_name = State()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "Kerakli bo‘limni tanlang:",
        reply_markup=menu
    )


@dp.message_handler(lambda message: message.text == "➕ Mijoz qo‘shish")
async def add_client_handler(message: types.Message):
    await message.answer("Mijoz nomini kiriting:")
    await AddClientState.waiting_name.set()


@dp.message_handler(state=AddClientState.waiting_name)
async def save_client_handler(message: types.Message, state: FSMContext):
    name = message.text.strip()

    result = add_client(name)

    if result:
        await message.answer(f"{name} bazaga qo‘shildi ✅", reply_markup=menu)
    else:
        await message.answer("Bu mijoz oldin qo‘shilgan ⚠️", reply_markup=menu)

    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
