from aiogram.dispatcher.filters.state import StatesGroup, State

# Состояния для алгоритма создания обсуждения
class Questions(StatesGroup):
    start = State()
    temp = State()
    answer = State()
    typeQ = State()
    topictheme = State()