from dataclasses import dataclass
from envparse import Env
import os

env = Env()

env.read_envfile()

TG_BOT_HOST = env.str(
    "TG_BOT_HOST"
)

TG_BOT_PORT = env.int(
    "TG_BOT_PORT"
)

DATABASE_URL = env.str(
    "DATABASE_URL",
    default='postgresql+asyncpg://yurii:YuriiPython21@0.0.0.0:5432/pierogowa'
)

BACKEND_URL = env.str(
    "BACKEND_URL",
    default='http://localhost:8000'
)

FRONTEND_URL = env.str(
    "FRONTEND_URL"
)

CURRENT_SERVER_STATUS = {"status": "close"}

TG_BOT_TOKEN = env.str(
    "TG_BOT_TOKEN"
)

ADMIN_LIST = {}

COOKS_LIST = {}

PASSWORD_ADMIN = env.str(
    "PASSWORD_ADMIN"
)

PASSWORD_COOK = env.str(
    "PASSWORD_COOK"
)

STORAGE_PHOTO_PATH = "/home/yurii/MainProjects/Pierogowa/tg_bot/media/"

IMGBB_API_KEY = env.str(
    "IMGBB_API_KEY"
)

TG_SERVER_URL = env.str(
    "TG_SERVER_URL"
)


BACKEND_ADMIN_NAME = env.str(
    "BACKEND_ADMIN_NAME"
)

BACKEND_ADMIN_PASSWORD = env.str(
    "BACKEND_ADMIN_PASSWORD"
)


@dataclass
class db_schemas:
    menu: str = 'menu'
