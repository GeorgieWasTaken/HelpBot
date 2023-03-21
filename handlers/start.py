from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards import menu,kouch_menu
from config import dp,db, bot, admin_id
import asyncpg.exceptions
"""кнопка старт"""


@dp.message_handler(Command('start'))
async def start(message: types.Message, state: FSMContext):
    try:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    if message.from_user.id==339925580:
        await message.answer(f"Админка, {message.from_user.username}", reply_markup=kouch_menu)

    else:
        await message.answer(f"Привет, {message.from_user.username}", reply_markup=menu)
