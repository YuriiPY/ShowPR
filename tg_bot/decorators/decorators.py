import asyncio
from functools import wraps
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode

from helpers.logging import bot_logger


def save_dialog_callback(start_state):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                bot_logger.exception(
                    f"❌ Error in Callback function {func.__module__}.{func.__name__}: {e}")

                message = None
                for arg in args:
                    if isinstance(arg, CallbackQuery):
                        message = arg.message
                        break
                    elif isinstance(arg, Message):
                        message = arg
                        break

                dialog_manager: DialogManager = None
                for arg in args:
                    if hasattr(arg, "dialog_data") and hasattr(arg, "start"):
                        dialog_manager = arg
                        break

                if message and dialog_manager:
                    await message.answer(f"Loose context in ({func.__module__}.{func.__name__}). Restarting dialog...")

                    await asyncio.sleep(2)
                    await dialog_manager.start(start_state, mode=StartMode.RESET_STACK)
        return wrapper
    return decorator


def save_dialog_getter(default: dict = {}):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                bot_logger.exception(
                    f"❌ Error in Getter function {func.__module__}.{func.__name__}: {e}")

                return default
        return wrapper
    return decorator
