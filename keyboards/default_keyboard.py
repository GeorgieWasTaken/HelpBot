from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, \
    KeyboardButton

from keyboards.callback_datas import km_callback, us_callback

# Кнопки для главного меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задать вопрос"),
            KeyboardButton(text="Назначить встречу"),
        ],

    ],
    resize_keyboard=True
)

# Кнопки для выбора предмета
coach = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ответить"),

        ],

    ],
    resize_keyboard=True
)

answer_on_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Личный"),
            KeyboardButton(text="Общий")
        ],
    ],
    resize_keyboard=True
)

stop_the_bot = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Остановить диалог")
        ],
    ],
    resize_keyboard=True

)


stop_create_test = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            KeyboardButton(text="Закончить создание теста", callback_data=km_callback.new(number_of_menu='7'))
        ]
    ]

)
# Кнопки для главного меню коуча

kouch_menu=InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Создать тест для персонала", callback_data=km_callback.new(number_of_menu='2'))

        ],
        [
            InlineKeyboardButton(text="Отправить тест персоналу", callback_data=km_callback.new(number_of_menu='3'))
        ],
        [
            InlineKeyboardButton(text="Создать рассылку для персонала", callback_data=km_callback.new(number_of_menu='4'))
        ],
        [
            InlineKeyboardButton(text="Создать диалог с сотрудником", callback_data=km_callback.new(number_of_menu='5'))
        ],
        [

            InlineKeyboardButton(text="Просмотреть результаты теста", callback_data=km_callback.new(number_of_menu='6'))
        ],

    ]
)



# Кнопки для создания личного вопроса
onepizda_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data=us_callback.new(number_of_user='1')),
            InlineKeyboardButton(text="2", callback_data=us_callback.new(number_of_user='2')),
            InlineKeyboardButton(text="3", callback_data=us_callback.new(number_of_user='3')),
            InlineKeyboardButton(text="4", callback_data=us_callback.new(number_of_user='4')),
            InlineKeyboardButton(text="5", callback_data=us_callback.new(number_of_user='5')),
            InlineKeyboardButton(text="6", callback_data=us_callback.new(number_of_user='6')),
            InlineKeyboardButton(text="7", callback_data=us_callback.new(number_of_user='7')),
            InlineKeyboardButton(text="8", callback_data=us_callback.new(number_of_user='8')),
            InlineKeyboardButton(text="9", callback_data=us_callback.new(number_of_user='9')),
            InlineKeyboardButton(text="10", callback_data=us_callback.new(number_of_user='10'))
        ],
    ]
)

