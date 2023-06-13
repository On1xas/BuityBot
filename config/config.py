from environs import Env
from dataclasses import dataclass

@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot

def load_config(path):
    env=Env()
    env.read_env(path=path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")))