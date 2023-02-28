import asyncio
import logging
from config import dp, bot, admin_id
from aiogram import types, executor
from keyboards import menu
import handlers


async def start_up(message=types.Message):
    await bot.send_message(chat_id=str(339925580), text="Бот запущен и готов к работе!",reply_markup=menu)
    await bot.send_message(chat_id=str(408576223), text="Бот запущен и готов к работе!", reply_markup=menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_up)
    asyncio.get_event_loop().run_forever()
