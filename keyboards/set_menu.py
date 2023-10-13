from aiogram import Bot
from aiogram.types import BotCommand


# Главное меню бота
async def set_main_menu(bot: Bot) -> None:
    # список команд и их описание для кнопки menu
    main_menu = [
        BotCommand(command="/start", description="Начало работы бота"),
        BotCommand(command="stream", description="Запуск видеопотока"),
        BotCommand(command="/getframe", description="Получить кадр"),
        BotCommand(command="/stop", description="Остановка видеопотока")
    ]

    await bot.set_my_commands(main_menu)
