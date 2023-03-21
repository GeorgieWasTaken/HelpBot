# мяу
import asyncio
import aiogram
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import Questions
from aiogram.dispatcher.filters import Text
from config import dp, db, bot, admin_id
from keyboards import answer_on_menu, menu, stop_the_bot, kouch_menu, answer_on_kouch_menu, question_for_all, question_for_one
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
    global question_type
    if message.text == "Личный":
        question_type = "Личный"
    else:
        question_type = "Общий"
    await message.answer("Какова тема?", reply_markup=ReplyKeyboardRemove())
    await Questions.typeQ.set()


@dp.message_handler(state=Questions.typeQ)
async def conv_start(message: types.Message):
    theme = message.text
    await message.answer("Создан чат с коучем. Задавайте вопрос", reply_markup=stop_the_bot)
    telegram_id = message.from_user.id
    Forum_topic = await bot.create_forum_topic(chat_id='@helpbot_bot_bot_bot',
                                               name=f"Тип вопроса-{question_type}: {theme}")
    topic_id = Forum_topic.message_thread_id
    await db.add_topic(
        topic_id=topic_id,
        telegram_id=telegram_id,
        question_type=question_type,
        theme=theme,
        is_active=True
    )

    await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic_id,
                           text="Сейчас будет задан анонимный вопрос")
    await Questions.start.set()


"""Юзер задает вопрос коучу + остановка бота для юзера"""


@dp.message_handler(state=Questions.start)
async def asking(message: types.Message, state: FSMContext):
    text = message.text

    topic_id=await db.select_topic_id(telegram_id=message.from_user.id, is_active=True)
    print(topic_id)
    topic_id=topic_id.get('topic_id')
    if text == "Остановить диалог":
        await message.answer('Чат удален', reply_markup=menu)
        await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic_id, text='Диалог остановлен')

        # вопрос юле
        # await bot.delete_forum_topic(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic)


        await db.update_is_active(is_active=False,topic_id=topic_id)
        await state.finish()

        return
    is_active = await db.select_is_active(topic_id=topic_id)
    if is_active.get('is_active')==True:

        await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic_id, text=text)



@dp.message_handler(is_admin=True)
async def answ(message: types.Message, state: FSMContext):
    text = message.text
    topic_id = message.message_thread_id
    is_active = await db.select_is_active(topic_id=topic_id)
    if is_active.get('is_active') == True:

        telegram_id=await db.select_user_id(topic_id=topic_id)
        telegram_id=telegram_id.get('telegram_id')

        await bot.send_message(chat_id=telegram_id, text=text)

    elif text == 'Задать вопрос персоналу':
                await message.answer("Выберите тип вопроса", reply_markup=answer_on_kouch_menu)
    elif text == 'Личный вопрос сотруднику':
                await message.reply("Выберите действие", reply_markup=question_for_one)
    elif text == 'Вопрос для всех':
                await message.reply("Выберите действие", reply_markup=question_for_all)


@dp.message_handler(content_types=['photo','video','video_note','voice'])
async def nudes(message: types.Message, state: FSMContext):
    topic_id = message.message_thread_id
    telegram_id = await db.select_user_id(topic_id=topic_id)
    telegram_id = telegram_id.get('telegram_id')
    is_active = await db.select_is_active(topic_id=topic_id)
    if is_active.get('is_active') == True:
        if message.photo:
                photo= message.photo[0].file_id
                await bot.send_photo(chat_id=telegram_id, photo=photo)



        if message.video:
            video = message.video.file_id
            await bot.send_video(chat_id=telegram_id, video=video)

        if message.video_note:
            video_note = message.video_note.file_id
            await bot.send_video_note(chat_id=telegram_id, video_note=video_note)

        if message.voice:
            voice = message.voice.file_id
            await bot.send_voice(chat_id=telegram_id, voice=voice)
    else:
        # await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic, text='Диалог остановлен')

        await state.finish()
        return