
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards import menu
from config import dp, bot, admin_id

"""кнопка старт"""
@dp.message_handler(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Это бот", reply_markup=menu)
