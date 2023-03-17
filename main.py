import aiogram
import asyncio
import logging
from config import dp,db, bot, admin_id
from aiogram import types, executor
from keyboards import menu
import handlers


async def start_up(message=types.Message):
    logging.info("Создаем подключение к базе данных")
    await db.create()

    logging.info("Создаем таблицу пользователей")
    await db.create_table_users()

    logging.info("Создаем таблицу топиков")
    await db.create_table_topics()

    logging.info("Готово")
    await bot.send_message(chat_id=str(339925580), text="Бот запущен и готов к работе!",reply_markup=menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_up)
    asyncio.get_event_loop().run_forever()
