from typing import Union

from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.callback_data import CallbackData


admin_router = Router()


class AdminCallback(CallbackData, prefix='admin'):
    level: int
    action: str


async def crate_admin_callback(level: int, action: str):
    return AdminCallback(level=level, action=action)
