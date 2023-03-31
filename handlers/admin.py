import asyncio
import aiogram
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import db, bot
from keyboards import kouch_menu, answer_on_kouch_menu, question_for_all, \
    question_for_one
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

@dp.callback_query_handler(text_contains='km')
async def next_menu(call: CallbackQuery):
    callback_data = call.data
    logging.info = (f"call = {callback_data}")
    if callback_data == 'km:1':
        await call.message.reply('Выберите тип ворпоса', reply_markup=answer_on_kouch_menu)
    elif callback_data == 'km:2':
        await call.message.reply('Выберите действие', reply_markup=question_for_one)
    elif callback_data == 'km:3':
        await call.message.reply('Выберите действие', reply_markup=question_for_all)
    elif callback_data == 'km:4':
        count=await db.count_users()
        for i in range(count):
            telegram_id=await db.select_user(id=i+1)
            telegram_id = telegram_id.get('telegram_id')
            print(telegram_id)
            await bot.send_message(chat_id=telegram_id,text="Оповещение всем")





    elif callback_data == 'km:5':
        await call.message.reply('Процедура создания тестов пока не готова, приносим свои извинения')
    elif callback_data == 'km:6':
        await call.message.reply('Процедура создания вопросов со стороны коуча пока не готова, приносим свои извинения')
    elif callback_data == 'km:7':
        await call.message.reply('Процедура создания тестов пока не готова, приносим свои извинения')


@dp.message_handler(is_admin=True)
async def answ(message: types.Message, state: FSMContext):
    text = message.text
    topic_id = message.message_thread_id
    if text == '1234ЮЛЯ':
        await message.answer("Здравствуйте, Юлия", reply_markup=kouch_menu)
    else:

        is_active = await db.select_is_active(topic_id=topic_id)
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