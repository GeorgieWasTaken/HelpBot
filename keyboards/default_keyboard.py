from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
