from aiogram.fsm.state import State, StatesGroup

class FSMFillForm(StatesGroup):
    fill_route = State()        # Состояние ожидания ввода имени
    fill_ride = State()         # Состояние ожидания ввода возраста
    registration = State()         # Состояние ожидания ввода возраста
    choose = State()         # Состояние ожидания ввода возраста
    cancel = State()         # Состояние ожидания ввода возраста

