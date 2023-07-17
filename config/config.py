from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin: list[int]
@dataclass
class Database:
    user: str
    password: str
    host: str
    database: str

@dataclass
class Config:
    tg_bot: TgBot
    database: Database




def load_config(path):
    env = Env()
    env.read_env(path=path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN"),
                     admin=list(map(int, env.list('ADMIN')))),
        database=Database(user=env("USER_DB"),
                          password=env("PASSWORD_DB"),
                          host=env("HOST"),
                          database=env("DATABASE"))
        )