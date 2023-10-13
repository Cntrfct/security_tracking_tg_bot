from aiogram import Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from stream.videostream import ChatVideoStreams, Videostream

router = Router(name="handlers_router")


@router.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer(text="<b>Добро пожаловать!</b>\n\n"
                          "Данный бот умеет управлять системой видеонаблюдения.\n"
                          "Воспользуйтесь кнопкой <b>'Меню'</b>")


# Запуск видеопотока
@router.message(Command(commands="stream"))
async def start_stream(
        msg: Message,
        bot: Bot,
        chat_video_streams: ChatVideoStreams,
) -> None:
    try:
        chat_video_streams.add_live_stream(
            chat_id=msg.chat.id,
            livestream=Videostream(chat_id=msg.chat.id, bot=bot),
        )

    except KeyError:
        await msg.answer(text="Видеопоток уже запущен!")
        return

    else:
        await msg.answer(text="Видеопоток запущен. . .")


# Остановка видеопотока
@router.message(Command(commands="stop"))
async def stop_stream(msg: Message, chat_video_streams: ChatVideoStreams) -> None:
    try:
        chat_video_streams.stop_live_stream(chat_id=msg.chat.id)

    except KeyError:
        await msg.answer(text="Видеопоток не запущен!")
        return

    else:
        await msg.answer(text="Видеопоток остановлен!")


# Сохранение и отправка кадра
@router.message(Command(commands="getframe"))
async def save_frame(msg: Message, chat_video_streams: ChatVideoStreams) -> None:
    try:
        livestream = chat_video_streams.get_live_stream(chat_id=msg.chat.id)

    except KeyError:
        await msg.answer(text="Видеопоток не запущен!")
        return

    else:
        await livestream.send_frame(msg)


# ответ на любой текст, кроме комманд
@router.message()
async def send_echo(msg: Message):
    await msg.answer(text=f'Я не понимаю, что значит {msg.text}\n'
                          'Пожалуйста, воспользуйтесь кнопкой "Меню".')
