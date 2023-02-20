import asyncio
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from environs import Env



env=Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
admin_id=env.str("ADMIN")
IP=env.str("ip")

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспатчера
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage = MemoryStorage())
loop=asyncio.get_event_loop()

