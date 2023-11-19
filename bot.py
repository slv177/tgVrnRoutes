import asyncio
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


async def main():
    storage = MemoryStorage()
    # Загружаем конфиг в переменную config
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await set_main_menu(bot)
    await dp.start_polling(bot)


# Функция конфигурирования и запуска бота
if __name__ == '__main__':
    asyncio.run(main())