from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

from config import ADMIN_ID
from db import get_user, add_user
from keyboards import main_menu
from aiogram import Bot

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot):
    user = await get_user(message.from_user.id)

    if user:
        if user["status"] == "approved":
            await message.answer("Xush kelibsiz ✅", reply_markup=main_menu())
        elif user["status"] == "pending":
            await message.answer("So‘rovingiz ko‘rib chiqilmoqda ⏳")
        else:
            await message.answer("Siz rad etilgansiz ❌")
        return

    await add_user(message.from_user.id, message.from_user.full_name)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve:{message.from_user.id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject:{message.from_user.id}")
        ]
    ])

    await bot.send_message(
        ADMIN_ID,
        f"🆕 Yangi foydalanuvchi:\n\n"
        f"{message.from_user.full_name}\n"
        f"ID: {message.from_user.id}",
        reply_markup=kb
    )

    await message.answer("So‘rovingiz yuborildi ⏳")