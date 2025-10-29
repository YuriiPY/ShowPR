from envparse import Env
import os

env = Env()

env.read_envfile()

NGINX_URL = env.str(
    "NGINX_URL",
    default='http://localhost:80'
)

DATABASE_URL = env.str(
    "DATABASE_URL"
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL"
)

FRONT_END_URL = env.str(
    "FRONT_END_URL",
    default='http://localhost:3000'
)

BACKEND_URL = env.str(
    "BACKEND_URL",
    default='http://localhost:8000'
)

TG_BOT_URL = env.str(
    "TG_BOT_URL"
)

BACKEND_HOST = env.str(
    "BACKEND_HOST",
    default='0.0.0.0'
)
BACKEND_PORT = env.int(
    "BACKEND_PORT",
    default=8000
)

ADMIN_NAME = env.str(
    "ADMIN_NAME"
)

ADMIN_PASSWORD = env.str(
    "ADMIN_PASSWORD"
)
