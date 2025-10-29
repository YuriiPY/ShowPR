import asyncio
from aiogram import Router
from aiogram.types import Update
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import StartMode
from aiogram_dialog.manager.bg_manager import BgManagerFactoryImpl

from helpers.logging import bot_logger
from helpers.message import delayed_delete_message
from bot.bot import bot, dp
from dialogs.admin.admin_states import AdminMenuSelection
from dialogs.cook.cook_states import CookMenuSelection
from services.admin import AdminServices
from services.cook import CookServices


error_router = Router()


@error_router.error()
async def global_error_controller(event: ErrorEvent):
    bot_logger.exception(f"⚠️ Unhandled exception: {event.exception} ")

    factory = BgManagerFactoryImpl(router=dp)

    update = event.update

    try:

        if update.message:
            user_id = update.message.from_user.id
            message = update.message

        elif update.callback_query:
            user_id = update.callback_query.from_user.id
            message = update.callback_query.message

        alert_message = await message.answer("⚠️ Something went wrong. I will write this problem to admins. \nRedirecting you to the home page ")
        await delayed_delete_message(alert_message, 2)

        if await AdminServices.get_admin(user_id) is not None:
            asyncio.create_task(
                factory.bg(
                    bot=bot,
                    user_id=user_id,
                    chat_id=user_id,
                ).start(
                    state=AdminMenuSelection.main_menu,
                    mode=StartMode.RESET_STACK
                )
            )
        elif await CookServices.get_cook(user_id) is not None:
            asyncio.create_task(
                factory.bg(
                    bot=bot,
                    user_id=user_id,
                    chat_id=user_id,
                ).start(
                    state=CookMenuSelection.main_menu,
                    mode=StartMode.RESET_STACK
                )
            )
    except Exception as e:
        bot_logger.exception(f"⚠️ Bot can`t send a error message to user: {e}")
