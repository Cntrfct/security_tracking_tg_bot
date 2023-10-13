from dataclasses import dataclass
from environs import Env


@dataclass
class TgBotConfig:
    token: str  # токен бота
    admin_ids: list[int]  # список админов бота


@dataclass
class DatabaseConfig:
    database: str  # название базы данных
    db_host: str  # адрес базы данных
    db_user: str  # имя пользователя бд
    dp_pass: str  # пароль к бд


@dataclass
class Config:
    tg_bot: TgBotConfig
    db: DatabaseConfig


# добавляем переменные окружения из .env
def load_config() -> Config:
    env: Env = Env()
    env.read_env()

    return Config(tg_bot=TgBotConfig(token=env("BOT_TOKEN"),
                                     admin_ids=list(map(int, env.list("ADMIN_IDS")))),
                  db=DatabaseConfig(database=env("DATABASE"),
                                    db_host=env("DB_HOST"),
                                    db_user=env("DB_USER"),
                                    dp_pass=env("DB_PASSWORD")))
