from dataclasses import dataclass
from environs import Env


@dataclass
class TgBotConfig:
    token: str  # токен бота


@dataclass
class Config:
    tg_bot: TgBotConfig


# добавляем переменные окружения из .env
def load_config() -> Config:
    env: Env = Env()
    env.read_env()

    return Config(tg_bot=TgBotConfig(token=env("BOT_TOKEN")))
