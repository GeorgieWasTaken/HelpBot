import asyncio
import aiogram
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import Questions
from aiogram.dispatcher.filters import Text
from config import dp, db, bot
from keyboards import answer_on_menu, menu, stop_the_bot
from aiogram.types import ReplyKeyboardRemove
from config import dp
#from aiogram.utils.callback_data import CallbackData
#from keyboards.callback_datas import km_callback

global smile
smile = {'Личный': "5370870893004203704", 'Общий': "5418115271267197333"}

@dp.message_handler(Text(equals=["Задать вопрос"]))
async def conv_start(message: types.Message):
    await message.answer("Какой тип вопроса?", reply_markup=answer_on_menu)
    await Questions.topictheme.set()


"""Бот задает тему диалога"""


@dp.message_handler(state=Questions.topictheme)
async def conv_start(message: types.Message):
    global question_type
    question_type = message.text
    if question_type == 'Личный' or question_type == 'Общий':
        await message.answer("Какова тема?", reply_markup=ReplyKeyboardRemove())
        await Questions.typeQ.set()
    else:
        await message.answer("Вы ввели несуществующий тип вопроса, введите заново")


@dp.message_handler(state=Questions.typeQ)
async def conv_start(message: types.Message):
    theme = message.text
    await message.answer("Создан чат с коучем. Задавайте вопрос", reply_markup=stop_the_bot)
    telegram_id = message.from_user.id
    Forum_topic = await bot.create_forum_topic(chat_id='@helpbot_bot_bot_bot',
                                               name=f"Тип вопроса-{question_type}: {theme}",
                                               icon_custom_emoji_id=smile[question_type])

    topic_id = Forum_topic.message_thread_id
    await db.add_topic(
        topic_id=topic_id,
        telegram_id=telegram_id,
        question_type=question_type,
        theme=theme,
        is_active=True
    )
    if question_type == "Личный":
        await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic_id,
                               text="Сейчас будет задан анонимный вопрос")
    else:
        await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic_id,
                               text=f"Сейчас будет задан вопрос от {message.from_user.username}")
    await Questions.start.set()


"""Юзер задает вопрос коучу + остановка бота для юзера"""


@dp.message_handler(state=Questions.start)
async def asking(message: types.Message, state: FSMContext):
    text = message.text

    topic_id = await db.select_topic_id(telegram_id=message.from_user.id, is_active=True)
    print(topic_id)
    topic_id = topic_id.get('topic_id')
    if text == "Остановить диалог":
        await message.answer('Диалог остановлен', reply_markup=menu)
        await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic_id, text='Диалог остановлен')

        # вопрос юле
        # await bot.delete_forum_topic(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic)

        await db.update_is_active(is_active=False, topic_id=topic_id)
        await state.finish()

        return
    is_active = await db.select_is_active(topic_id=topic_id)

    if is_active.get('is_active') == True:
        await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic_id, text=text)
