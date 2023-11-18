from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.create_keyboard import create_inline_kb
from lexicon.lexicon import LEXICON_RU
from external_services.external_services import get_routes, get_rides
from filters.filters import IsDigitCallbackData

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


@router.message(Command(commands='routes'))
async def process_routes_command(message: Message):
    routes = get_routes()
    keyboard = create_inline_kb(1, **routes)
    await message.answer(text=LEXICON_RU['/routes'], reply_markup=keyboard)

@router.callback_query(IsDigitCallbackData())
async def process_route_press(callback: CallbackQuery):
    print("маршрут: ", callback.data)
    rides = get_rides(callback.data)
    keyboard = create_inline_kb(1,  **rides)
    print(keyboard)
    await callback.message.edit_reply_markup(reply_markup=keyboard, text="Рейсы выбранного маршрута")

