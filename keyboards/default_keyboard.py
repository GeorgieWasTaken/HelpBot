
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
