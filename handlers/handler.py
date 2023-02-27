#мяу
import aiogram
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import Questions
from aiogram.dispatcher.filters import Text
from config import dp, bot, admin_id
from keyboards import answer_on_menu, menu, stop_the_bot
from aiogram.types import ReplyKeyboardRemove
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

"""Бот спрашивает, к какому типу относится вопрос"""


@dp.message_handler(Text(equals=["Задать вопрос"]))
async def conv_start(message: types.Message):
    await message.answer("Какой тип вопроса?", reply_markup=answer_on_menu)
    await Questions.topictheme.set()


"""Бот задает тему диалога"""


@dp.message_handler(state=Questions.topictheme)
async def conv_start(message: types.Message):
    global typeQ
    if message.text == "Личный":
        typeQ = "Личный"
    else:
        typeQ = "Общий"
    await message.answer("Какова тема?", reply_markup=ReplyKeyboardRemove())
    await Questions.typeQ.set()


@dp.message_handler(state=Questions.typeQ)
async def conv_start(message: types.Message):
    theme = message.text

    await message.answer("Создан чат с коучем. Задавайте вопрос", reply_markup=stop_the_bot)
    global user_id
    user_id = message.from_user.id
    global topic
    Forum_topic = await bot.create_forum_topic(chat_id='@helpbot_bot_bot_bot', name=f"Тип вопроса-{typeQ}: {theme}")
    topic = Forum_topic.message_thread_id
    await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic,
                           text="Сейчас будет задан анонимный вопрос")
    await Questions.start.set()


"""Юзер задает вопрос коучу"""


# @dp.message_handler(state=Questions.start)
# async def asking(message: types.Message, state: FSMContext):
#     text = message.text
#
#     if text == "Отмена":
#         await message.answer('Чат удален', reply_markup=menu)
#         await state.finish()
#         return
#
#     await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic, text=text)


"""Сообщения от админа, которые бот берет из топика и отправляет юзеру"""


@dp.message_handler(is_admin=True)
async def answ(message: types.Message):
    text = message.text
    await bot.send_message(chat_id=user_id, text=text)


"""Остановка бота"""


@dp.message_handler(Text(equals=["Остановить бота"]))
async def stopping(message: types.Message):
    await message.answer('Чат удален', reply_markup=menu)





