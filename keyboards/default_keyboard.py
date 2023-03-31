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

# Кнопки для главного меню коуча

kouch_menu = InlineKeyboardMarkup(
        inline_keyboard=[
        [
            InlineKeyboardButton(text="Задать вопрос персоналу", callback_data=km_callback.new(number_of_menu='1'))
        ],
    ]
)

# Кнопки для выбора типа вопроса для коуча
answer_on_kouch_menu=InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Личный вопрос сотруднику", callback_data=km_callback.new(number_of_menu='2')),
            InlineKeyboardButton(text="Вопрос для всех", callback_data=km_callback.new(number_of_menu='3'))
        ],
    ]
)

# Кнопки для создания вопроса для всех
question_for_all = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Создать оповещение",callback_data=km_callback.new(number_of_menu='4')),
            InlineKeyboardButton(text="Создать тест", callback_data=km_callback.new(number_of_menu='5'))
        ],
    ]
)


# Кнопки для создания личного вопроса
question_for_one = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Задать личный вопрос", callback_data=km_callback.new(number_of_menu='6')),
            InlineKeyboardButton(text="Создать тест", callback_data=km_callback.new(number_of_menu='7'))
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