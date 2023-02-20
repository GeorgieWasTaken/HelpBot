import aiogram
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import Questions
from aiogram.dispatcher.filters import Text
from config import dp, bot, admin_id


from config import dp

"""Фильтр на сообщения от админа"""
from aiogram.dispatcher.filters import BoundFilter
class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()

dp.filters_factory.bind(MyFilter)

"""Открытие чата с коучем"""
@dp.message_handler(Text(equals=["Задать вопрос"]))
async def conv_start(message:types.Message):
    await message.answer('Создан чат с коучем. Задавайте вопрос')
    global user_id
    user_id=message.from_user.id
    global topic
    Forum_topic = await bot.create_forum_topic(chat_id='@helpbot_bot_bot_bot',name='Аноним')
    topic=Forum_topic.message_thread_id
    await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic, text="Сейчас будет задан анонимный вопрос")
    await Questions.start.set()

"""Юзер задает вопрос коучу"""
@dp.message_handler(state=Questions.start)
async def asking(message:types.Message, state: FSMContext):
    text = message.text

    if text=="Отмена":
        await message.answer('Чат удален')
        await state.finish()
        return

    await bot.send_message(chat_id='@helpbot_bot_bot_bot',message_thread_id=topic, text=text)




"""Сообщения от админа"""
@dp.message_handler(is_admin=True)
async def answ(message:types.Message):

        text = message.text
        await bot.send_message(chat_id=user_id, text=text)






