import asyncio
import aiogram
import logging
import argparse
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import db, bot
from states import Admin, Tests
from keyboards import kouch_menu, stop_create_test
from aiogram.types import CallbackQuery
from config import dp
#from aiogram.utils.callback_data import CallbackData
#from keyboards.callback_datas import km_callback

from aiogram.dispatcher.filters import BoundFilter


class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


dp.filters_factory.bind(MyFilter)

@dp.message_handler(is_admin=True)
async def answ(message: types.Message, state: FSMContext):
    text = message.text
    topic_id = message.message_thread_id
    if text == '1234ЮЛЯ':
        await message.answer("Здравствуйте, Юлия", reply_markup=kouch_menu)
    else:

        is_active = await db.select_is_active(topic_id=topic_id)
        if is_active is not None:
            if is_active.get('is_active') == True:
                telegram_id = await db.select_user_id(topic_id=topic_id)
                telegram_id = telegram_id.get('telegram_id')

                await bot.send_message(chat_id=telegram_id, text=text)


@dp.message_handler(content_types=['photo', 'video', 'video_note', 'voice'])
async def nudes(message: types.Message, state: FSMContext):
    topic_id = message.message_thread_id
    telegram_id = await db.select_user_id(topic_id=topic_id)
    telegram_id = telegram_id.get('telegram_id')
    is_active = await db.select_is_active(topic_id=topic_id)
    if is_active.get('is_active') == True:
        if message.photo:
            photo = message.photo[0].file_id
            await bot.send_photo(chat_id=telegram_id, photo=photo)



        elif message.video:
            video = message.video.file_id
            await bot.send_video(chat_id=telegram_id, video=video)

        elif message.video_note:
            video_note = message.video_note.file_id
            await bot.send_video_note(chat_id=telegram_id, video_note=video_note)

        elif message.voice:
            voice = message.voice.file_id
            await bot.send_voice(chat_id=telegram_id, voice=voice)
    else:
        # await bot.send_message(chat_id='@helpbot_bot_bot_bot', message_thread_id=topic, text='Диалог остановлен')

        await state.finish()
        return

@dp.callback_query_handler(text_contains='km')
async def next_menu(call: CallbackQuery):
    callback_data = call.data
    logging.info = (f"call = {callback_data}")
    if callback_data == 'km:2':
        await call.message.answer('Введите название нового теста')
        await Tests.new.set()
    elif callback_data == 'km:3':
        await call.message.reply('Процедура просмотра результатов тестов пока что не работает')
    elif callback_data == 'km:4':
        await Admin.onlyfans.set()
        await call.message.answer('Введите текст рассылки')
    elif callback_data == 'km:5':
        await call.message.reply('Процедура создания личных диалогов пока не работает')
    elif callback_data == 'km:6':
        await call.message.answer('Процедура отправления тестов пока не работает')


@dp.message_handler(state=Admin.onlyfans)
async def pido(message:types.Message, state: FSMContext):
    text=message.text
    count = await db.count_users()
    print(count)
    for i in range(count):
        telegram_id = await db.select_user(id=i + 1)
        print(telegram_id)
        print(i)
        telegram_id = telegram_id.get('telegram_id')

        await bot.send_message(chat_id=telegram_id, text=f"Общая рассылка!\n{text}")
        await message.answer('Сообщение отправлено')
    await state.finish()

@dp.message_handler(state=Admin.onepizda)
async def ras(message:types.Message, state: FSMContext):
    text=message.text
    count = await db.count_users()
    for i in range(count):
        telegram_id = await db.select_user(id=2)
        telegram_id = telegram_id.get('telegram_id')
        print(telegram_id)
        await bot.send_message(chat_id=telegram_id, text=f"Общая рассылка!\n{text}")
        await message.answer('Сообщение отправлено')
    await state.finish()

@dp.message_handler(state=Tests.new)
async def newtest(message:types.Message, state: FSMContext):
    name=message.text
    n=await db.select_max_test_id()
    hui=str(n[0])
    if hui.find('None')==hui.find('=')+1:
        m=0
    else:
        m=int(hui[hui.find('=')+1:hui.find('>')])
    await db.add_test(m+1,name)
    await message.answer('Введите вопрос', reply_markup=stop_create_test)
    await Tests.createq.set()

@dp.message_handler(state=Tests.createq)
async def creatingq(message:types.Message, state: FSMContext):
    text=message.text
    if text=='Закончить создание теста':
        await message.answer('Тест успешно создан', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        n = await db.select_max_test_id()
        hui = str(n[0])
        m = int(hui[hui.find('=') + 1:hui.find('>')])
        await db.add_test(m,text)
        await message.answer('Введите ответ на вопрос', reply_markup=types.ReplyKeyboardRemove())
        await Tests.createa.set()

@dp.message_handler(state=Tests.createa)
async def creatinga(message:types.Message, state: FSMContext):
    text=message.text
    if text=='Закончить создание теста':
        await message.answer('Введите ответ на вопрос, чтобы закончить создание теста')
    else:
        n = await db.select_max_id()
        hui = str(n[0])
        m = int(hui[hui.find('=') + 1:hui.find('>')])
        await db.add_a(m,text)
        await message.answer('Введите вопрос', reply_markup=stop_create_test)
        await Tests.createq.set()