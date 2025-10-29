import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.main import set_bot_commands
from core.config import TG_BOT_TOKEN
from dialogs.admin.admin_dialogs import main_admin_menu

dp = Dispatcher()
bot = Bot(TG_BOT_TOKEN)
