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

# Кнопки для главного меню коуча
kouch_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задать вопрос"),
        ],

    ],
    resize_keyboard=True
)

# Кнопки для выбора типа вопроса для коуча
answer_on_kouch_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Личный вопрос"),
            KeyboardButton(text="Вопрос всем"),
        ],

    ],
    resize_keyboard=True
)

# Кнопки для создания вопроса для всех
question_for_all = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать оповещение"),
            KeyboardButton(text="Создать тест"),
        ],

    ],
    resize_keyboard=True
)

# Кнопки для создания личного вопроса
question_for_one = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задать личный вопрос"),
            KeyboardButton(text="Создать тест"),
        ],

    ],
    resize_keyboard=True
)