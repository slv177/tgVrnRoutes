from aiogram.fsm.state import State, StatesGroup

class FSMFillForm(StatesGroup):
    fill_route = State()        # Состояние ожидания ввода имени
    fill_ride = State()         # Состояние ожидания ввода возраста

