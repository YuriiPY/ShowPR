from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/help", description="Help"),
    ]
    await bot.set_my_commands(commands)