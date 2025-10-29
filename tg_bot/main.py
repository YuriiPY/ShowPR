import asyncio
from typing import List
from aiogram.fsm.storage.base import StorageKey
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi import Request, FastAPI, HTTPException
from contextlib import asynccontextmanager
from aiohttp import web
from aiogram import types, Dispatcher, Bot
from aiogram.types import Message, User, Chat, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiogram_dialog.manager.bg_manager import BgManagerFactoryImpl

import bot.run
from dialogs.admin import admin_callbacks, admin_dialogs, admin_getters, admin_states
from dialogs.cook import cook_callbacks, cook_dialogs, cook_getters, cook_getters
from dialogs.cook.cook_states import Cook_Order
from bot.bot import bot, dp
from core.config import TG_SERVER_URL, TG_BOT_TOKEN, TG_BOT_HOST, TG_BOT_PORT
from db.crud.users.crud import _get_items_from_table_by_models
from db.models.users.admin import Admin
from db.models.users.cook import Cooks
from dialogs.admin.admin_states import Admin_Order
from dialogs.cook.cook_states import Cook_Order
from schemas.products import OrderRequest
from db.session import database_connection_test


app = FastAPI()
WEBHOOK_PATH = f"/bot/{TG_BOT_TOKEN}"
WEBHOOK_URL = f"{TG_SERVER_URL}{WEBHOOK_PATH}"


def get_commands_ru():
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/help", description="Помощь"),
    ]
    return commands


def get_commands_en():
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/help", description="Help"),
    ]
    return commands


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(get_commands_ru(), scope=types.BotCommandScopeAllPrivateChats(), language_code="ru")
    await bot.set_my_commands(get_commands_en(), scope=types.BotCommandScopeAllPrivateChats(), language_code="en")


async def set_webhook():
    await bot.set_webhook(WEBHOOK_URL)


async def handle_webhook(request: Request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]

    if token == TG_BOT_TOKEN:
        update = types.Update(**await request.json())
        await dp.feed_webhook_update(bot, update)
        return web.Response()
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


async def handle_some_webhook(order_list: List[str], order_id: int):
    factory = BgManagerFactoryImpl(router=dp)

    button = [
        [InlineKeyboardButton(text="Show orders", callback_data="show orders")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=button)

    order_list_string = ''
    for index, order_name in enumerate(order_list):
        order_list_string += f'{index+1}. {order_name} \n'

    try:
        cooks = await _get_items_from_table_by_models(
            Table=Cooks,
            filter_column="status",
            filter_column_data=True
        )
        admins = await _get_items_from_table_by_models(
            Table=Admin,
            filter_column="status",
            filter_column_data=True
        )

        users = cooks + admins

        if not users:
            admins = await _get_items_from_table_by_models(
                Table=Admin
            )
            await asyncio.gather(*[
                bot.send_message(chat_id=admin.telegram_id,
                                 text=f"🟥A new order has arrived but no one is working🟥 \nNew order: \n{order_list_string}", reply_markup=keyboard)
                for admin in admins
            ])
            return

        try:
            await asyncio.gather(*[
                asyncio.create_task(factory.bg(
                    bot=bot,
                    user_id=admin.telegram_id,
                    chat_id=admin.telegram_id
                ).start(
                    state=Admin_Order.warning_window,
                    data={
                        'warning_data': order_list,
                        'order_id': order_id
                    },
                    mode=StartMode.RESET_STACK))
                for admin in admins
            ])
            await asyncio.gather(*[
                asyncio.create_task(factory.bg(
                    bot=bot,
                    user_id=cook.telegram_id,
                    chat_id=cook.telegram_id
                ).start(
                    state=Cook_Order.warning_window,
                    data={
                        'warning_data': order_list,
                        'order_id': order_id
                    },
                    mode=StartMode.RESET_STACK))
                for cook in cooks
            ])

        except Exception as e:
            print(str(e))

    except Exception as e:
        print(str(e))


async def on_startup():
    await set_webhook()
    await set_default_commands(bot)
    await database_connection_test()


if __name__ == "__main__":
    app.add_event_handler("startup", on_startup)

    @app.post(WEBHOOK_PATH)
    async def webhook_endpoint(request: Request):
        return await handle_webhook(request)

    @app.post("/bot/new_msg")
    async def send_new_msg(order_data: OrderRequest):
        await handle_some_webhook(order_data.order_list, order_data.order_id)
        print(order_data)

    import uvicorn

    uvicorn.run(app, host=TG_BOT_HOST, port=TG_BOT_PORT)
