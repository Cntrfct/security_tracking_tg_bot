from aiogram import Bot, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from stream.videostream import ChatVideoStreams, Videostream

# роутер обработки хэндлеров
router = Router(name="handlers_router")


# группа состояний для выбора источника
class UserState(StatesGroup):
    choosing_input = State()


# обработка команды старт
@router.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer(text="<b>Добро пожаловать!</b>\n\n"
                          "Данный бот умеет управлять системой видеонаблюдения.\n"
                          "Воспользуйтесь кнопкой <b>'Меню'</b>")


# запустить состояние выбора источника видеопотока
@router.message(Command(commands="stream"))
async def start_stream(msg: Message, state: FSMContext) -> None:
    await msg.answer(text="Введите источник камеры:")
    await state.set_state(UserState.choosing_input)


# этот хэндлер принимает целое число, для выбора вэб-камеры
@router.message(UserState.choosing_input, F.text.cast(int).as_("cam_id"))
async def set_input_int(msg: Message,
                        bot: Bot,
                        state: FSMContext,
                        cam_id: int,
                        chat_video_streams: ChatVideoStreams) -> None:
    try:
        chat_video_streams.add_live_stream(
            chat_id=msg.chat.id,
            livestream=Videostream(chat_id=msg.chat.id, bot=bot, cam_id=cam_id),
        )

    except KeyError:
        await msg.answer(text="Видеопоток уже запущен!")
        return

    else:
        await msg.answer(text="Видеопоток запущен. . .")

    finally:
        await state.clear()


# этот хэндлер принимает ссылку на поток
@router.message(UserState.choosing_input, F.text.startswith(('http:', 'https:', 'rtsp:')), F.text.as_("cam_id"))
async def set_input_str(msg: Message,
                        bot: Bot,
                        state: FSMContext,
                        cam_id: str,
                        chat_video_streams: ChatVideoStreams) -> None:
    try:
        chat_video_streams.add_live_stream(
            chat_id=msg.chat.id,
            livestream=Videostream(chat_id=msg.chat.id, bot=bot, cam_id=cam_id),
        )

    except KeyError:
        await msg.answer(text="Видеопоток уже запущен!")
        return

    else:
        await msg.answer(text="Видеопоток запущен. . .")

    finally:
        await state.clear()


# этот хэндлер сообщает о некорректно введенном источнике
@router.message(UserState.choosing_input)
async def set_input_incorrectly(msg: Message):
    await msg.answer(text="<b>Источник введён не корректно!</b>\n\n"
                          "Пожалуйста, введите <b>цифру</b>(например <b>0</b>) для вэб-камеры\n"
                          "или <b>ссылку</b> для подключения к удаленному видеопотоку")


# остановить видеопоток
@router.message(Command(commands="stop"))
async def stop_stream(msg: Message, chat_video_streams: ChatVideoStreams) -> None:
    try:
        chat_video_streams.stop_live_stream(chat_id=msg.chat.id)

    except KeyError:
        await msg.answer(text="Видеопоток не запущен!")
        return

    else:
        await msg.answer(text="Видеопоток остановлен!")


# сохранение и отправка кадра
@router.message(Command(commands="getframe"))
async def save_frame(msg: Message, chat_video_streams: ChatVideoStreams) -> None:
    try:
        livestream = chat_video_streams.get_live_stream(chat_id=msg.chat.id)

    except KeyError:
        await msg.answer(text="Видеопоток не запущен!")
        return

    else:
        await livestream.send_frame(msg)
