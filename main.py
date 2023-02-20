import asyncio
import logging
from config import dp, bot, admin_id
from aiogram import types, executor




import handlers


async def start_up(message=types.Message):

    """await bot.send_message(chat_id=admin_id, text="Бот запущен и готов к работе")"""

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_up)
    asyncio.get_event_loop().run_forever()