import asyncio
from datetime import datetime
from io import BytesIO
import base64
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
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

from helpers.message import delayed_delete_message
from services.admin import AdminServices
from services.storage import *
from dialogs.admin.admin_states import (
    Admin_Confirm,
    AdminMenuSelection,
    Server,
    Admin_Menu,
    Cooks,
    Admin_Order
)
from db.crud.users.crud import _delete_item_by_id, _get_items_from_table_by_models, _update_item_data, _get_item_by_name, _update_user_data_by_telegram_id
from db.models.orders.orders import Orders
import core.config as config
from db.models.users.admin import Admin
from decorators.decorators import save_dialog_callback


def check_level_admin(
    data: Data,
    widget: Start,
    dialog_manager: DialogManager,
):

    return data.get("admin_information").level >= 3


async def get_back_dialog(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    await dialog_manager.start(AdminMenuSelection.main_menu, mode=StartMode.RESET_STACK)


@save_dialog_callback(start_state=AdminMenuSelection.main_menu)
async def store_click(
    callback_query: Union[CallbackQuery, any],
    dialog_manager: DialogManager,
    action: Callable,
    widget_id: str,
    kwargs: dict,
):
    admin_information = config.ADMIN_LIST.get(callback_query.from_user.id)

    action_list = {
        "open_store": "Do you really want to open the store ?",
        "close_store": "Do you really want to close the store ?"
    }
    await dialog_manager.start(Admin_Confirm.Confirm, data={
        "action_name": action_list.get(widget_id, ""),
        "next_state": Server.Server,
        "action": action,
        "kwargs": kwargs
    }, mode=StartMode.NORMAL)


@save_dialog_callback(start_state=AdminMenuSelection.main_menu)
async def confirm_action(
    callback_query: CallbackQuery,
    dialog_manager: DialogManager,
):

    action: Callable | None = dialog_manager.start_data.get("action", None)
    next_state = dialog_manager.start_data.get("next_state", None)
    next_state_data = dialog_manager.start_data.get("next_state_data", {})
    args = dialog_manager.start_data.get("args", [])
    kwargs = dialog_manager.start_data.get("kwargs", {})

    if action is not None:
        try:
            result = await action(*args, **kwargs)
            # print(result)
            await callback_query.message.edit_text(f"🛜 {result.get('func_status')}", )
            await asyncio.sleep(1)

        except Exception as ex:
            print(f"Error action: {ex}")

    if next_state:
        await dialog_manager.start(next_state, data={**next_state_data}, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.done()


@save_dialog_callback(start_state=AdminMenuSelection.main_menu)
async def cancel_action(
    callback_query: CallbackQuery,
    dialog_manager: DialogManager
):
    action_to_cancel: Callable | None = dialog_manager.start_data.get(
        "action_to_cancel", None)
    next_state = dialog_manager.start_data.get("next_state", None)
    next_state_data = dialog_manager.start_data.get("next_state_data", {})
    args = dialog_manager.start_data.get("args_to_cancel", [])
    kwargs = dialog_manager.start_data.get("kwargs_to_cancel", {})

    print("ACTION FOR CANCEL", action_to_cancel)
    if action_to_cancel is not None:
        print("CANCEL ACTION IS WORK", kwargs)
        try:
            result = await action_to_cancel(*args, **kwargs)
            await callback_query.message.edit_text(f"❗️ {result.get('func_status')}")
            await asyncio.sleep(1)

        except Exception as ex:
            print(f"Error action: {ex}")

    print("NEXT STATE", type(next_state), next_state)
    if next_state:
        await dialog_manager.start(next_state, data={**next_state_data}, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.done()


@save_dialog_callback(start_state=Admin_Menu.menu)
async def selected_menu_item(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str,
):
    if item_id.split(":")[0] == " ":
        return
    dialog_manager.dialog_data["current_schema"] = item_id.split(":")[0]
    dialog_manager.dialog_data["current_table"] = item_id.split(":")[1]
    await dialog_manager.switch_to(Admin_Menu.delicious_menu)


@save_dialog_callback(start_state=Admin_Menu.menu)
async def selected_dish(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str,
):
    dialog_manager.dialog_data["current_dish"] = item_id

    if int(item_id) == 0:
        dialog_manager.dialog_data["action"] = "New name for item:"
        await dialog_manager.switch_to(Admin_Menu.add_new_dish_menu)
    else:
        await dialog_manager.switch_to(Admin_Menu.current_dish_menu)


@save_dialog_callback(start_state=Admin_Menu.menu)
async def current_dish_button(
        Callback_query: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        item_column: str,
):
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
    await dialog_manager.switch_to(Admin_Menu.last_menu_window)


# async def price_button(
#         Callback_query: CallbackQuery,
#         widget: Button,
#         dialog_manager: DialogManager
# ):
#     dialog_manager.dialog_data["item_column"] = "price"
#     dialog_manager.dialog_data[
#         "action"] = f"""{dialog_manager.dialog_data.get("dish_information")["name"]}
# Current price: {dialog_manager.dialog_data.get("dish_information")["price"]}
# For change write a new one below: """
#     await dialog_manager.switch_to(Menu.last_menu_window)


# async def description_button(
#         Callback_query: CallbackQuery,
#         widget: Button,
#         dialog_manager: DialogManager
# ):
#     dialog_manager.dialog_data["item_column"] = "description"
#     dialog_manager.dialog_data[
#         "action"] = f"""{dialog_manager.dialog_data.get("dish_information")["name"]}
# Current description: {dialog_manager.dialog_data.get("dish_information")["description"]}
# For change write a new one below: """
#     await dialog_manager.switch_to(Menu.last_menu_window)


# async def status_button(
#         Callback_query: CallbackQuery,
#         widget: Button,
#         dialog_manager: DialogManager
# ):
#     dialog_manager.dialog_data["item_column"] = "status"
#     dialog_manager.dialog_data["status_action"] = dialog_manager.dialog_data.get(
#         "dish_information")["status"]
#     dialog_manager.dialog_data[
#         "action"] = f"""{dialog_manager.dialog_data.get("dish_information")["name"]}
# Current status: {dialog_manager.dialog_data.get("dish_information")["status"]}"""
#     await dialog_manager.switch_to(Menu.last_menu_window)

@save_dialog_callback(start_state=Admin_Menu.menu)
async def photo_button(
    Callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
):
    dialog_manager.dialog_data["item_column"] = "img"
    dialog_manager.dialog_data["status_action"] = "img"
    dialog_manager.dialog_data[
        "action"] = f"""Change photo for {dialog_manager.dialog_data.get("dish_information")["name"]}"""
    await dialog_manager.switch_to(Admin_Menu.last_menu_window)


@save_dialog_callback(start_state=Admin_Menu.menu)
async def delete_button(
        Callback_query: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data[
        "action_name"] = f"""remove {dialog_manager.dialog_data.get("dish_information")["name"]}"""
    await dialog_manager.back()
    await dialog_manager.start(Admin_Confirm.Confirm, data={
        "action_name": f"""remove {dialog_manager.dialog_data.get("dish_information")["name"]}""",
        "action": _delete_item_by_id,
        "kwargs": {"schema_name": dialog_manager.dialog_data["current_schema"],
                   "table_name": dialog_manager.dialog_data["current_table"],
                   "item_id": dialog_manager.dialog_data["dish_information"]["id"], }
    }, mode=StartMode.NORMAL
    )


@save_dialog_callback(start_state=Admin_Menu.menu)
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
            if not await name_filter(message, dialog_manager):
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
        value = await save_photo(file_data, current_table+str(item_id))

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


@save_dialog_callback(start_state=Admin_Menu.menu)
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


@save_dialog_callback(start_state=Admin_Menu.menu)
async def handle_input_for_create(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        value: any = None,
):
    field_map = [
        "name",
        "name_ua",
        "name_pl",
        "price",
        "description",
        "description_ua",
        "description_pl",
        "type",
        "status",
        "img"
    ]

    reply_text = {
        "name": "❌ This name is already exists! \nPlease enter a new name: ",
        "price": "❌ Price requires a numeric value \nPlease enter a valid price:",
        "type": "❌ Please choose the product type:",
        "status": "❌ Please choose the product status:",
        "img": "❌ Please send a valid photo:"
    }

    current_field_index = int(
        dialog_manager.dialog_data.get("current_field_index", 0))
    current_field = field_map[current_field_index]
    fields = dialog_manager.dialog_data.setdefault("fields", {})
    dialog_manager.dialog_data["action"] = ""
    dialog_manager.dialog_data["error_value"] = None

    # print("FIRST SEND =>", "CURRENT_FIELD =>",
    #       current_field, "FIELDS =>", fields)

    async def validate_field(field, value):
        if field == "name":
            return await name_filter(message, dialog_manager)
        elif field == "price":
            return value.isdigit()
        elif field == "type":
            return value in ["by weight", "by portion"]
        elif field == "status":
            return value in ["✅Active", "❌Inactive"]
        elif field == "img":
            return bool(message.photo)
        return True

    async def process_field(field, value):
        if field == "price":
            return int(value)
        elif field == "status":
            return True if value == "✅Active" else False
        elif field == "img":

            file_data = await message.bot.get_file(message.photo[-1].file_id)
            value = file_data.file_path
            # FIXME: THE BACK-END SERVER CAN`T SEND A NONE IMG, AND CAUSE CHECK DB FOR NOT REQUIRED, BE STRONG!
            # if new_item:
            #     print("new_item:", new_item, current_table, new_item.get("id"))
            #     file_info = await message.bot.get_file(message.photo[-1].file_id)
            #     dialog_manager.dialog_data["current_img_info"] = file_info
            #     file_data = await message.bot.download_file(file_info.file_path)

            #     value = await save_photo(file_data, current_table+"/"+str(new_item.get("id")))
            #     dialog_manager.dialog_data["dish_information"] = new_item
        return value

    if type(message) == Message:
        if not await validate_field(current_field, message.text if current_field != "img" else message.photo):
            dialog_manager.dialog_data["error_value"] = "❌ Wrong value!"
            await message.reply(reply_text.get(current_field, "❌ Wrong value!"))
            return

    input_value = value if isinstance(message, CallbackQuery) else (
        message.photo if current_field == "img" else message.text)
    fields[current_field] = await process_field(current_field, input_value)

    current_field_index += 1
    dialog_manager.dialog_data["current_field_index"] = current_field_index
    dialog_manager.dialog_data["fields"] = fields

    if current_field_index >= len(field_map):
        current_schema = dialog_manager.dialog_data.get(
            "current_schema", "menu")
        current_table = dialog_manager.dialog_data.get("current_table", "")

        await dialog_manager.start(Admin_Confirm.Confirm, data={
            "action_name": f"""Create new Item with new fields?\n{ chr(10).join(f'{key}: {value if key != "img" else "Image added!"}' for key, value in fields.items())}""",
            "next_state": Admin_Menu.delicious_menu,
            "next_state_data": {
                "current_schema": current_schema,
                "current_table": current_table
            },
            "action": last_save_product,
            "kwargs": {
                "message": message,
                "dialog_data": dialog_manager.dialog_data
            }
            # BECAUSE FIRST WE CREATE A NEW ELEMENT IN THE DB TO GET THE ID, AND AFTER THAT WE CREATE A FILE TO DISPLAY THE NEW ELEMENT
        }, mode=StartMode.RESET_STACK)
    else:
        next_field = field_map[current_field_index]
        next_action_prompts = {
            "name": "Write the product name in Ukrainian:",
            "name_ua": "Write the product name in Polish:",
            "name_pl": "Write the price for the product:",
            "price": "Write the product description in English:",
            "description": "Write the product description in Ukrainian:",
            "description_ua": "Write the product description in Polish:",
            "description_pl": "Select product type:",
            "type": "Select product status:",
            "status": "Send a photo for the product:"
        }

        dialog_manager.dialog_data["action"] = next_action_prompts[current_field]
        await dialog_manager.switch_to(Admin_Menu.add_new_dish_menu)


async def last_save_product(
        message: Message,
        # dialog_manager: DialogManager
        dialog_data: dict
):
    current_schema = dialog_data.get("current_schema", "menu")
    current_table = dialog_data.get("current_table", "")
    fields = dialog_data.get("fields")

    result = await AdminServices.create_new_item_in_db(current_table, fields)
    print(result)
    new_item = result.get("new_item")
    new_item_id = new_item.get("id")

    file_data = await message.bot.download_file(fields.get("img"))
    img_url = await save_photo(file_data, current_table+"/"+str(new_item_id))
    print(img_url)

    function_result = await _update_item_data(current_schema, current_table, new_item_id, {"img": img_url})
    print(function_result)

    return function_result


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


async def incorrectly_written_data(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        value: any,
):
    await message.reply("Incorrectly written data, please try again:")


@save_dialog_callback(start_state=Cooks.cooks_list)
async def selected_cook(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str,
):
    dialog_manager.dialog_data["selected_cook"] = item_id
    await dialog_manager.switch_to(Cooks.current_cook)


@save_dialog_callback(start_state=Cooks.cooks_list)
async def change_level(
        Callback_query: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        new_level: int,
):

    await dialog_manager.start(Admin_Confirm.Confirm, data={
        "action_name": f"""change level to {dialog_manager.dialog_data.get("current_cook").cook_name} on {new_level}""",
        "next_state": Cooks.current_cook,
        "next_state_data": dialog_manager.dialog_data,
        "action": AdminServices.change_level_status,
        "kwargs": {"table_name": "cooks",
                   "user_telegram_id": dialog_manager.dialog_data.get("selected_cook"),
                   "new_level": new_level,
                   }
    }, mode=StartMode.NORMAL
    )


@save_dialog_callback(start_state=Cooks.cooks_list)
async def current_cook_btn(
        Callback_query: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        current_action: str
):
    cook_name = dialog_manager.dialog_data.get(
        "current_cook"
    ).cook_name

    action_text = {
        "write": f"Write a message to {cook_name}",
        "level": f"Change level to {cook_name}"
    }
    dialog_manager.dialog_data["status_action"] = action_text.get(
        current_action, "Something wrong!")
    await dialog_manager.switch_to(Cooks.last_cook_window)


@save_dialog_callback(start_state=Cooks.cooks_list)
async def write_message(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        value: str,
):
    telegram_user_id = dialog_manager.dialog_data.get(
        "current_cook").telegram_id
    await AdminServices.send_message_to_cook(
        dialog_manager=dialog_manager, user_id=telegram_user_id, message_text=value)
    await dialog_manager.switch_to(Cooks.current_cook)


@save_dialog_callback(start_state=AdminMenuSelection.main_menu)
async def log_out(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
):
    config.ADMIN_LIST.pop(callback_query.from_user.id)
    user_id = callback_query.from_user.id
    await _update_user_data_by_telegram_id(
        user_table=Admin,
        telegram_id=user_id,
        item_data={
            "logged_in": False
        }
    )
    await callback_query.message.answer("You are logged out")
    await dialog_manager.reset_stack()


@save_dialog_callback(start_state=Admin_Order.main_window)
async def selected_order(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    dialog_manager.dialog_data["current_order_id"] = item_id

    await dialog_manager.switch_to(Admin_Order.current_order)


@save_dialog_callback(start_state=Admin_Order.main_window)
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

    await dialog_manager.switch_to(Admin_Order.current_dish_information)


@save_dialog_callback(start_state=AdminMenuSelection.main_menu)
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
        await dialog_manager.start(state=Admin_Order.main_window, mode=StartMode.RESET_STACK, data={
            "orders": orders
        })
    else:
        sended_message = await callback_query.message.answer("No orders today yet")
        asyncio.create_task(delayed_delete_message(sended_message, 2))


@save_dialog_callback(start_state=Admin_Order.main_window)
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
        state=Admin_Confirm.Confirm,
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


@save_dialog_callback(start_state=AdminMenuSelection.main_menu)
async def show_new_order(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    order_id = dialog_manager.start_data.get('order_id')

    await dialog_manager.start(
        state=Admin_Order.current_order,
        data={
            'order_id': order_id
        },
        mode=StartMode.RESET_STACK)
