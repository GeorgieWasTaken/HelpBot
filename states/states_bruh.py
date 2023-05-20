from aiogram.dispatcher.filters.state import StatesGroup, State


# Состояния для алгоритма создания обсуждения
class Questions(StatesGroup):
    start = State()
    temp = State()
    answer = State()
    typeQ = State()
    topictheme = State()
    closedialogue = State()

class Admin(StatesGroup):
    onlyfans=State()
    oprosec=State()
    onepizda=State()

class Tests(StatesGroup):
    new=State()
    createq=State()
    createa=State()
    otpravit=State()