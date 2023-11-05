from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    token: str  # токен бота


# добавляем переменные окружения из .env
def load_config() -> Config:
    env: Env = Env()
    env.read_env()

    return Config(token=env("BOT_TOKEN"))
