from datetime import datetime
from aiogram.types import WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram import F
import asyncio
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message
from aiogram_dialog import Data, DialogManager, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Next,
    Row,
    ScrollingGroup,
    Select,
    Start,
)
from typing import Optional, Callable, Union

import jwt

from bot.bot import dp
from helpers.message import delayed_delete_message
from dialogs.cook.cook_states import Cook_Settings, CookMenuSelection, Cook_Order, Work, Cook_Confirm, Cook_Menu
from services.cook import CookServices
from db.crud.users.crud import (
    _delete_item_by_id,
    _get_items_from_table_by_models,
    _update_item_data,
    _get_item_by_name,
    _update_user_data_by_telegram_id
)
from db.base import Base
from db.models.orders.orders import Orders
from db.models.users.cook import Cooks
from services.storage import save_photo
from core.config import COOKS_LIST
from decorators.decorators import save_dialog_callback


@save_dialog_callback(start_state=CookMenuSelection.main_menu)
async def confirm_action(
    callback_query: CallbackQuery,
    dialog_manager: DialogManager,
):

    action: Callable | None = dialog_manager.start_data.get("action")
    next_state = dialog_manager.start_data.get("next_state", "")
    next_state_data = dialog_manager.start_data.get("next_state_data", {})
    args = dialog_manager.start_data.get("args", [])
    kwargs = dialog_manager.start_data.get("kwargs", {})

    if action is not None:
        try:
            result = await action(*args, **kwargs)
            # print(result)
            await callback_query.message.edit_text(f"🛜 {result.get('func_status')}", )
            await asyncio.sleep(2)

        except Exception as ex:
            print(f"Error action: {ex}")

    if next_state:
        await dialog_manager.start(next_state, data={**next_state_data}, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.done()


@save_dialog_callback(start_state=CookMenuSelection.main_menu)
async def cancel_action(
    callback_query: CallbackQuery,
    dialog_manager: DialogManager
):
    action_to_cancel: Callable | None = dialog_manager.start_data.get(
        "action_to_cancel", None)
    next_state = dialog_manager.start_data.get("next_state", None)
    next_state_data = dialog_manager.start_data.get("next_state_data", None)
    args = dialog_manager.start_data.get("args_to_cancel", [])
    kwargs = dialog_manager.start_data.get("kwargs_to_cancel", {})

    print("ACTION FOR CANCEL", action_to_cancel)
    if action_to_cancel is not None:
        print("CANCEL ACTION IS WORK", kwargs)
        try:
            result = await action_to_cancel(*args, **kwargs)
            await callback_query.message.edit_text(f"❗️ {result.get('func_status')}")
            await asyncio.sleep(2)

        except Exception as ex:
            print(f"Error action: {ex}")

    if next_state:
        await dialog_manager.start(next_state, data={**next_state_data}, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.done()


async def get_back_dialog(callback_query: CallbackQuery, button: Button,
                          dialog_manager: DialogManager,):
    await dialog_manager.start(CookMenuSelection.main_menu, mode=StartMode.RESET_STACK)


location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send verification",
                        request_location=True,
                        )]],
    resize_keyboard=True,
    one_time_keyboard=True
)


@save_dialog_callback(start_state=Work.main_work)
async def send_verification(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):

    sent_message = await callback_query.message.answer("Verification❗️", reply_markup=location_keyboard)
    dialog_manager.dialog_data["verify_message"] = sent_message
    dialog_manager.dialog_data["location_sended"] = True


@save_dialog_callback(start_state=Work.main_work)
async def finish_working_day(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    await dialog_manager.start(Cook_Confirm.Confirm, data={
        "action_name": "Do you really wanna end the workday?",
        "action": CookServices.handle_cook_day,
        "next_state": CookMenuSelection.main_menu,
        "kwargs": {
            "telegram_id": callback_query.from_user.id,
            "work_status": False
        }
    })


@dp.message(F.content_type == ContentType.LOCATION)
@save_dialog_callback(start_state=Work.main_work)
async def handle_location(message: Message, state: FSMContext, dialog_manager: DialogManager):

    if dialog_manager.dialog_data.get("location_sended", False):
        dialog_manager.dialog_data["verify_location"] = False
        dialog_manager.dialog_data.get("verify_message").delete()
        lat = message.location.latitude
        lon = message.location.longitude

        if await CookServices.check_cook_location(lat, lon):
            if await CookServices.handle_cook_day(message.from_user.id, True):
                sent_message = await message.answer("Let`s start to work✅", reply_markup=ReplyKeyboardRemove())

                asyncio.create_task(delayed_delete_message(sent_message, 2))
                await dialog_manager.start(CookMenuSelection.main_menu, mode=StartMode.RESET_STACK)
            else:
                msg = await message.answer("Are you trying to work second time today?", reply_markup=ReplyKeyboardRemove())
                asyncio.create_task(delayed_delete_message(msg, 2))

        else:
            await message.answer("You can start work only in restaurant", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("why you send location to me?")

# Menu CallBack


@save_dialog_callback(start_state=Cook_Menu.menu)
async def selected_menu_item(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str,
):
    dialog_manager.dialog_data["current_schema"] = item_id.split(":")[0]
    dialog_manager.dialog_data["current_table"] = item_id.split(":")[1]
    await dialog_manager.switch_to(Cook_Menu.delicious_menu)


@save_dialog_callback(start_state=Cook_Menu.menu)
async def selected_dish(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str,
):
    dialog_manager.dialog_data["current_dish"] = item_id

    if int(item_id) == 0:
        dialog_manager.dialog_data["action"] = "New name for item:"
        await dialog_manager.switch_to(Cook_Menu.add_new_dish_menu)
    else:
        await dialog_manager.switch_to(Cook_Menu.current_dish_menu)


@save_dialog_callback(start_state=Cook_Menu.menu)
async def current_dish_button(
        Callback_query: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        item_column: str,
):

    if await CookServices.cook_level_check(
        Callback_query,
        dialog_manager,
        Cook_Menu.menu,
        2
    ):
        return

    dish_inform = dialog_manager.dialog_data.get("dish_information")
    name = dish_inform["name"]
    current_value = dish_inform[item_column]

    dialog_manager.dialog_data["item_column"] = item_column

    if item_column == "status":
        dialog_manager.dialog_data["status_action"] = current_value
        action_text = f"Current status: {current_value}"
    elif item_column == "img":
        dialog_manager.dialog_data["status_action"] = "img"
        action_text = f"""To change the photo for {name}, send a new photo:"""
    else:
        action_text = f"    {name}\nCurrent {item_column}: {current_value}\nFor change write a new one below:"

    dialog_manager.dialog_data["action"] = action_text
    await dialog_manager.switch_to(Cook_Menu.last_menu_window)


@save_dialog_callback(start_state=Cook_Menu.menu)
async def delete_button(
        Callback_query: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):

    await CookServices.cook_level_check(
        Callback_query,
        dialog_manager,
        Cook_Menu.menu,
        2
    )

    dialog_manager.dialog_data[
        "action_name"] = f"""remove {dialog_manager.dialog_data.get("dish_information")["name"]}"""
    await dialog_manager.back()
    await dialog_manager.start(Cook_Confirm.Confirm, data={
        "action_name": f"""remove {dialog_manager.dialog_data.get("dish_information")["name"]}""",
        "action": _delete_item_by_id,
        "kwargs": {"schema_name": dialog_manager.dialog_data["current_schema"],
                   "table_name": dialog_manager.dialog_data["current_table"],
                   "item_id": dialog_manager.dialog_data["dish_information"]["id"], }
    }, mode=StartMode.NORMAL
    )


@save_dialog_callback(start_state=Cook_Menu.menu)
async def change_data_item(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager
):
    current_schema = dialog_manager.dialog_data.get("current_schema")
    current_table = dialog_manager.dialog_data.get("current_table")
    item_column = dialog_manager.dialog_data.get("item_column")
    item_id = dialog_manager.dialog_data.get("current_dish")

    if value := message.text:
        if item_column == "name":
            if not await name_filter:
                await message.reply(f"This name {message.text} is already exist \nPlease enter a new name:")
                return

        elif item_column == "price":
            if value.isdigit():
                value = int(value)

            else:
                await message.reply("Price requires a numeric value \nPlease enter a valid price:")
                return

            # try:
            #     value = int(value)
            # except:
            #     await message.reply("Price requires a numeric value \nPlease enter a valid price:")
            #     return

    elif message.photo:
        print("photo\n")
        file_info = await message.bot.get_file(message.photo[-1].file_id)
        file_data = await message.bot.download_file(file_info.file_path)
        value = save_photo(file_data, current_table+str(item_id))

    if item_column is not None:
        result = await _update_item_data(
            schema_name=current_schema,
            table_name=current_table,
            item_column=item_column,
            item_id=item_id,
            item_data=value
        )

    await message.answer(result["func_status"])
    await asyncio.sleep(1)
    await dialog_manager.back()


@save_dialog_callback(start_state=Cook_Menu.menu)
async def change_status_item(
        message: Message,
        widget: Button,
        dialog_manager: DialogManager
):
    current_schema = dialog_manager.dialog_data.get("current_schema")
    current_table = dialog_manager.dialog_data.get("current_table")
    item_column = dialog_manager.dialog_data.get("item_column")
    item_id = dialog_manager.dialog_data.get("current_dish")

    status = "❌" in dialog_manager.dialog_data.get("dish_information")[
        "status"]

    if not item_column:
        raise KeyError

    result = await _update_item_data(
        schema_name=current_schema,
        table_name=current_table,
        item_column=item_column,
        item_id=item_id,
        item_data=status
    )

    await message.answer(result["func_status"])
    await asyncio.sleep(1)

    await dialog_manager.back()


@save_dialog_callback(start_state=Cook_Menu.menu)
async def name_filter(
        message: Message,
        dialog_manager: DialogManager
):
    current_schema = dialog_manager.dialog_data.get("current_schema")
    current_table = dialog_manager.dialog_data.get("current_table")

    item = await _get_item_by_name(current_schema, current_table, message.text)

    if not item:
        return True
    else:
        return False


@save_dialog_callback(start_state=Cook_Settings.main_settings)
async def log_out(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    COOKS_LIST.pop(callback_query.from_user.id)
    user_id = callback_query.from_user.id
    await _update_user_data_by_telegram_id(
        user_table=Cooks,
        telegram_id=user_id,
        item_data={
            "logged_in": False
        }
    )
    await callback_query.message.answer("You are logged out")
    await dialog_manager.reset_stack()


@save_dialog_callback(start_state=Cook_Order.main_window)
async def selected_order(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    dialog_manager.dialog_data["current_order_id"] = item_id

    await dialog_manager.switch_to(Cook_Order.current_order)


@save_dialog_callback(start_state=Cook_Order.main_window)
async def selected_order_product(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    order = dialog_manager.dialog_data.get("current_order")

    dialog_manager.dialog_data["current_schema"] = "menu"
    dialog_manager.dialog_data["current_table"] = order.items[int(
        item_id)].get("table_name", "")
    dialog_manager.dialog_data["current_dish"] = order.items[int(
        item_id)].get("id", 0)

    await dialog_manager.switch_to(Cook_Order.current_dish_information)


@save_dialog_callback(start_state=CookMenuSelection.main_menu)
async def open_orders(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    current_date = datetime.now().date()

    orders = await _get_items_from_table_by_models(
        Table=Orders,
        order_by=["delivery_time"],
        filter_column="delivery_date",
        filter_column_data=current_date
    )

    if orders:
        await dialog_manager.start(state=Cook_Order.main_window, mode=StartMode.NORMAL, data={
            "orders": orders
        })
    else:
        sended_message = await callback_query.message.answer("No orders today yet")
        asyncio.create_task(delayed_delete_message(sended_message, 2))


@save_dialog_callback(start_state=Cook_Order.main_window)
async def handle_order_status(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    current_order = dialog_manager.dialog_data.get("current_order")

    updated_order_status = {
        "pending": "processing",
        "processing": "ready to delivery",
        "ready to delivery": ""
    }
    action_name = {
        "pending": "Accept the order❓",
        "processing": "Mark as cooked❓"
    }
    await dialog_manager.start(
        state=Cook_Confirm.Confirm,
        mode=StartMode.NORMAL,
        data={
            "action_name": action_name.get(current_order.status),
            "action": _update_item_data,
            "kwargs": {
                "schema_name": "order_data",
                "table_name": "orders",
                "item_id": current_order.id,
                "item_column": "status",
                "item_data": updated_order_status.get(current_order.status)
            }
        }
    )
