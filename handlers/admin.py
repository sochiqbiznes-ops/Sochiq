from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

from config import ADMIN_ID
from db import update_status
from keyboards import main_menu

router = Router()

@router.callback_query(F.data.startswith("approve"))
async def approve_handler(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        return

    user_id = int(callback.data.split(":")[1])

    await update_status(user_id, "approved")

    await bot.send_message(
        user_id,
        "✅ Siz tasdiqlandingiz!",
        reply_markup=main_menu()
    )

    await callback.message.edit_text("✅ Tasdiqlandi")


@router.callback_query(F.data.startswith("reject"))
async def reject_handler(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        return

    user_id = int(callback.data.split(":")[1])

    await update_status(user_id, "rejected")

    await bot.send_message(user_id, "❌ Siz rad etildingiz")

    await callback.message.edit_text("❌ Rad etildi")