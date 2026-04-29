import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy import select

# Fayllarni bog'lash
from database import init_db, async_session, Customer
from states import CRMStates

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- TUGMALAR ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="➕ Mijoz qo‘shish")
    builder.row(types.KeyboardButton(text="👥 Mijozlar"), types.KeyboardButton(text="📊 Hisobot"))
    return builder.as_markup(resize_keyboard=True)

def customer_card_kb(cust_id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📦 Topshirish", callback_data=f"take_{cust_id}"))
    builder.row(types.InlineKeyboardButton(text="💳 To‘lov", callback_data=f"pay_{cust_id}"))
    builder.row(types.InlineKeyboardButton(text="💰 Narx belgilash", callback_data=f"price_{cust_id}"))
    return builder.as_markup()

# --- HANDLERLAR ---
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("🧠 CRM Botga xush kelibsiz!", reply_markup=main_menu())

@dp.message(F.text == "➕ Mijoz qo‘shish")
async def add_cust_start(message: types.Message, state: FSMContext):
    await message.answer("Mijoz ismini yozing:")
    await state.set_state(CRMStates.waiting_customer_name)

@dp.message(CRMStates.waiting_customer_name)
async def add_cust_finish(message: types.Message, state: FSMContext):
    async with async_session() as session:
        new_c = Customer(name=message.text)
        session.add(new_c)
        await session.commit()
    await message.answer(f"✔ {message.text} qo‘shildi", reply_markup=main_menu())
    await state.clear()

@dp.message(F.text == "👥 Mijozlar")
async def list_customers(message: types.Message):
    async with async_session() as session:
        res = await session.execute(select(Customer))
        customers = res.scalars().all()
    
    if not customers:
        await message.answer("Mijozlar ro'yxati bo'sh.")
        return

    builder = InlineKeyboardBuilder()
    for c in customers:
        builder.row(types.InlineKeyboardButton(text=c.name, callback_data=f"view_{c.id}"))
    await message.answer("Mijozni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("view_"))
async def view_profile(callback: types.CallbackQuery):
    c_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        c = await session.get(Customer, c_id)
        qarz = (c.taken * c.price) - c.paid
        text = (f"👤 **{c.name}**\n\n📦 Olingan: {c.taken} dona\n💰 Narx: {c.price} so‘m\n"
                f"💳 To‘langan: {c.paid} so‘m\n----------------------\n"
                f"❌ Qarz: {qarz} so‘m\n💰 Balans: -{qarz} so‘m")
        await callback.message.edit_text(text, reply_markup=customer_card_kb(c_id), parse_mode="Markdown")

@dp.callback_query(F.data.regexp(r"^(take|pay|price)_(\d+)$"))
async def handle_actions(callback: types.CallbackQuery, state: FSMContext):
    action, c_id = callback.data.split("_")
    await state.update_data(c_id=int(c_id), action=action)
    msgs = {"take": "Nechta dona berildi?", "pay": "Necha so'm to'ladi?", "price": "1 dona uchun narxni kiriting:"}
    await callback.message.answer(msgs[action])
    if action == "take": await state.set_state(CRMStates.waiting_take_count)
    elif action == "pay": await state.set_state(CRMStates.waiting_pay_amount)
    elif action == "price": await state.set_state(CRMStates.waiting_price_value)

@dp.message(CRMStates.waiting_take_count)
@dp.message(CRMStates.waiting_pay_amount)
@dp.message(CRMStates.waiting_price_value)
async def process_inputs(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, faqat raqam kiriting!")
        return
    
    data = await state.get_data()
    async with async_session() as session:
        c = await session.get(Customer, data['c_id'])
        val = int(message.text)
        if data['action'] == "take": c.taken += val
        elif data['action'] == "pay": c.paid += val
        elif data['action'] == "price": c.price = val
        await session.commit()
    await message.answer("✅ Ma'lumot saqlandi!", reply_markup=main_menu())
    await state.clear()

@dp.message(F.text == "📊 Hisobot")
async def total_report(message: types.Message):
    async with async_session() as session:
        res = await session.execute(select(Customer))
        customers = res.scalars().all()
    
    txt = "📊 **UMUMIY HISOBOT:**\n\n"
    total_qarz = 0
    for c in customers:
        qarz = (c.taken * c.price) - c.paid
        txt += f"👤 {c.name} → {qarz} so‘m\n"
        total_qarz += qarz
    txt += f"\n💥 **Jami qarz: {total_qarz} so‘m**"
    await message.answer(txt, parse_mode="Markdown")

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())