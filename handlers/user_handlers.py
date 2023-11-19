from aiogram import Router
from aiogram.types import Message, CallbackQuery
from keyboards.create_keyboard import create_inline_kb, create_registration_kb
from lexicon.lexicon import LEXICON_RU
from external_services.external_services import get_routes, get_rides, get_route_name, get_ride_time
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
             'Чтобы перейти к выбору маршрута и рейса\n'
             'отправьте команду /route'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.message(Command(commands='route'), StateFilter(default_state))
async def process_route_command(message: Message, state: FSMContext):

    routes = get_routes()
    markup = create_inline_kb(1, **routes)
    await state.update_data(first_name=message.from_user.first_name)
    await state.update_data(last_name=message.from_user.last_name)
    await state.update_data(full_name=message.from_user.full_name)
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(username=message.from_user.username)

    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Выберите маршрут',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора рейса

    await state.set_state(FSMFillForm.fill_ride)


@router.callback_query(StateFilter(FSMFillForm.fill_ride))
async def process_route_press(callback: CallbackQuery, state: FSMContext):
    chosenRoute = callback.data
    await state.update_data(route_id=chosenRoute)
    chosenRide = get_rides(chosenRoute)
    keyboard = create_inline_kb(1,  **chosenRide)
    await state.update_data(route_name=get_route_name(chosenRoute))

    await callback.message.edit_text(text=f'Выберите рейс маршрута "{get_route_name(chosenRoute)}"')
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await state.set_state(FSMFillForm.registration)


@router.callback_query(StateFilter(FSMFillForm.registration))
async def process_ride_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(ride_id=callback.data)
    keyboard = create_registration_kb()
    ride_detail = await state.get_data()
    await state.update_data(ride_time=get_ride_time(ride_detail['route_id'], callback.data))
    print("3", await state.get_state())
    print("4", await state.get_data())
    ride_detail = await state.get_data()
    await callback.message.edit_text(text=f'Будете регистрироваться на рейс в {ride_detail["ride_time"]} маршрута "{ride_detail["route_name"]}"? \n Осталось Х мест.')
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await state.set_state(FSMFillForm.choose)


@router.callback_query(StateFilter(FSMFillForm.choose))
async def process_choose_press(callback: CallbackQuery, state: FSMContext):
    print("process_choose_press", callback.data)
    if callback.data == "registration":
        print("rr")
    if callback.data == "cancel":
        await callback.message.edit_text(
            text='Вы сбросили настройки\n\n'
                 'Чтобы перейти к выбору маршрута и рейса\n'
                 'отправьте команду /route'
        )
        # Сбрасываем состояние и очищаем данные, полученные внутри состояний
        await state.clear()



