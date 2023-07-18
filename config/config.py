from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list[int]
    masters: list[int]
@dataclass
class SQLDatabase:
    user: str
    password: str
    host: str
    port: str
    database: str
    driver: str

@dataclass
class Redis:
    host: str
    port: str
    database: str

@dataclass
class Config:
    tg_bot: TgBot
    database: SQLDatabase
    redis: Redis


def load_config(path):
    env = Env()
    env.read_env(path=path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN"),
                     admins=list(map(int, env.list('ADMIN'))),
                     masters=list(map(int, env.list('MASTER')))
                     ),
        database=SQLDatabase(user=env("USER_DB"),
                          password=env("PASSWORD_DB"),
                          host=env("HOST"),
                          port=env("PORT"),
                          database=env("DATABASE"),
                          driver=env("DRIVER")
                          ),
        redis=Redis(host=env("REDIS_HOST"),
                    port=env("REDIS_PORT"),
                    database=env("REDIS_PORT")
        ))