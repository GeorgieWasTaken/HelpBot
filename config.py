import asyncio
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from environs import Env
from utils.db_api.postgresql import Database
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
admin_id = env.str("ADMIN")
IP = env.str("ip")

DB_USER=env.str("DB_USER")
DB_PASS=env.str("DB_PASS")
DB_NAME=env.str("DB_NAME")
DB_HOST=env.str("DB_HOST")
DB_PORT=env.str("DB_PORT")
# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспатчера
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
loop = asyncio.get_event_loop()

db=loop.run_until_complete(Database.create())