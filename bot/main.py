import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import Config, load_config
from stream.videostream import ChatVideoStreams
from handlers import user_handlers
from keyboards.set_menu import set_main_menu

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)


# инициализация бота и диспетчера, регистрация роутера
async def main() -> None:
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=MemoryStorage(), chat_video_streams=ChatVideoStreams())
    dp.include_router(router=user_handlers.router)
    # удаляем обновления, добавляем кнопку меню, запускаем бота в режиме поллинга
    await bot.delete_webhook(drop_pending_updates=True)
    await set_main_menu(bot)
    await dp.start_polling(bot)


# точка входа, запуск бота
if __name__ == '__main__':
    asyncio.run(main())
