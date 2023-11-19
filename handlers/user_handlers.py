from aiogram import Router
from aiogram.types import Message, CallbackQuery
from keyboards.create_keyboard import create_inline_kb
from lexicon.lexicon import LEXICON_RU
from external_services.external_services import get_routes, get_rides
from filters.filters import IsDigitCallbackData
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from states.states import FSMFillForm


# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Показываем доступные маршруты
@router.message(Command(commands='routes'))
async def process_routes_command(message: Message):
    routes = get_routes()
    keyboard = create_inline_kb(1, **routes)
    await message.answer(text=LEXICON_RU['/routes'], reply_markup=keyboard)

# Показываем рейсы выбранного маршрута
@router.callback_query(IsDigitCallbackData())
async def process_route_press(callback: CallbackQuery):
    rides = get_rides(callback.data)
    keyboard = create_inline_kb(1,  **rides)
    await callback.message.edit_text(text="Рейсы выбранного маршрута")
    await callback.message.edit_reply_markup(reply_markup=keyboard)

@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот позволит вам зарегистрироваться на поездку.\n\n'
             'Чтобы начать работу отправьте команду /fillform'
    )


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Вы еще не начали работу с ботом. \n\n'
             'Чтобы перейти к выбору маршрута и рейса'
             'отправьте команду /route'
    )


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы сбросили настройки\n\n'
             'Чтобы перейти к выбору маршрута и рейса'
             'отправьте команду /route'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.message(Command(commands='route'), StateFilter(default_state))
async def process_route_command(message: Message, state: FSMContext):

    routes = get_routes()
    markup = create_inline_kb(1, **routes)

    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Укажите маршрут',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора рейса
    await state.set_state(FSMFillForm.fill_ride)


@router.callback_query(StateFilter(FSMFillForm.fill_ride))
async def process_route_press(callback: CallbackQuery, state: FSMContext):
    chosenRoute = callback.data
    print(chosenRoute)

    chosenRide = get_rides(chosenRoute)
    print(chosenRide)
    keyboard = create_inline_kb(1,  **chosenRide)
    await callback.message.edit_text(text="Рейсы выбранного маршрута")
    await callback.message.edit_reply_markup(reply_markup=keyboard)
