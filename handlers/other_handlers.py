from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def send_echo(message: Message):
    print("send_echo", message)
    try:
        await message.reply(text=LEXICON_RU['unknown'])
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])