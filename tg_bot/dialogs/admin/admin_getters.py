import base64
from dataclasses import dataclass
from io import BytesIO
from itertools import zip_longest
import os
from urllib.parse import urljoin
import aiofiles
import requests

from aiogram_dialog import Dialog, DialogManager
from aiogram.types import CallbackQuery, Message, InputFile, FSInputFile, BufferedInputFile, FSInputFile, URLInputFile
from aiogram_dialog.widgets.kbd import Button
from datetime import datetime, timedelta
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
    Group
)
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram.enums import ContentType

from services.admin import AdminServices
from services.storage import *
from db.crud.users.crud import (
    _get_tables_in_schema,
    _get_items_from_table,
    _get_item_by_id,
    _get_items_from_table_by_models,
)
from db.models.users.cook import Cooks
from db.models.orders.orders import Orders
import core.config as config
from decorators.decorators import save_dialog_getter


@dataclass
class TimeSLot:
    id: int
    show_text: str
    time: str


@dataclass
class Cooks_l:
    id: int
    cook_name: str
    level: int
    telegram_id: int
    status: str

    @property
    def status_text(self):
        return 'Active✅' if self.status else 'Inactive❌'


async def get_admin_data(dialog_manager: DialogManager, **kwargs):
    admin_id = dialog_manager.middleware_data.get("event_from_user").id

    if admin_id not in config.ADMIN_LIST:
        admin_information = await AdminServices.get_admin(kwargs.get('event_from_user').id)
        config.ADMIN_LIST[admin_id] = admin_information
        # dialog_manager.dialog_data["admin_information"] = admin_information

        print("--------------------------------------------------------------------------", config.ADMIN_LIST)
    else:

        print("================================CONFIG_LIST================================")

    print(config.ADMIN_LIST)
    return {"admin_information":  config.ADMIN_LIST.get(admin_id)}


@save_dialog_getter(default={
    "server_status": "unknown",
    "store_status": "unknown"
})
async def checking_server_status(dialog_manager: DialogManager, **kwargs):
    current_status = {}

    try:
        async with httpx.AsyncClient() as client:
            url = urljoin(config.BACKEND_URL, f'store/status')
            response = await client.get(url=url)

            data = response.json() if response.status_code == 200 else {}

            current_status["server_status"] = "✅Online"if response.status_code == 200 else "❌Offline"

            print("data from store/status", data)

            if data["until"]:
                current_status["store_status"] = f"❌Store is close until {data["until"]}"
            elif data["isOpen"]:
                current_status["store_status"] = "✅Store is open"
            else:
                current_status["store_status"] = "❌Store is close before open"

            dialog_manager.dialog_data["store_status"] = data["isOpen"]

    except requests.RequestException as e:
        print(e)
        current_status["server_status"] = "❌ Request failed"
        current_status["store_status"] = "❌ Store status unavailable"
        # optionally: log.error(f"Error checking server status: {e}")

    except Exception as e:
        print(e)
        current_status["server_status"] = "⁉️ Something went wrong"
        current_status["store_status"] = "❌ Store status unavailable"

    return current_status


@save_dialog_getter(default={
    "time_slots": "unknown"
})
async def get_possible_close_time(dialog_manager: DialogManager, **kwargs):
    current_time = datetime.now()
    intervals = [
        TimeSLot(id=0, show_text="Close before open", time="CL_BE_OP")]

    for i in range(1, 9):
        current_time += timedelta(minutes=15)
        intervals.append(TimeSLot(id=i, show_text=current_time.strftime(
            "%H:%M"), time=current_time.strftime("%H:%M")))

    return {"time_slots": intervals}


@save_dialog_getter(default={
    "menu_buttons": "unknown"
})
async def get_tables(dialog_manager: DialogManager, **kwargs):
    print(kwargs.get("state"))
    schema, menu = await _get_tables_in_schema(schema=config.db_schemas.menu)

    cooked_menu = [item for item in menu if not item.startswith("frozen_")]
    frozen_menu = [item for item in menu if item.startswith("frozen_")]

    buttons = []

    for cooked_item, frozen_item in zip_longest(cooked_menu, frozen_menu):
        buttons.append({"button_name": cooked_item, "schema": schema}
                       if cooked_item else {"button_name": " ", "schema": " "})

        buttons.append({"button_name": frozen_item, "schema": schema}
                       if frozen_item else {"button_name": " ", "schema": " "})

    return {"menu_buttons": buttons}


@save_dialog_getter(default={
    "menu_items": "unknown"
})
async def get_table_items(dialog_manager: DialogManager, **kwargs):
    current_table: str = dialog_manager.dialog_data.get("current_table")
    if (current_schema := dialog_manager.dialog_data.get("current_schema")) is None:
        current_schema: str = dialog_manager.start_data.get("current_schema")
        current_table: str = dialog_manager.start_data.get("current_table")
        dialog_manager.dialog_data.update(dialog_manager.start_data)

    menu_items = [{
        "id": 0,
        "index": "",
        "item_name": "Add a new one product",
        "active": ""
    }]

    data = await _get_items_from_table(schema_name=current_schema, table_name=current_table, columns=["id",  "name", "status"])

    for index, item in enumerate(data):
        menu_items.append({
            "id": item[0],
            "index": index+1,
            "item_name": item[1],
            "active": "✅Active" if item[2] == True else "❌Inactive"
        })

    # print(menu_items)
    return {"menu_items": menu_items}


@save_dialog_getter(default={
    "dish_information": "unknown",
    "photo": "unknown"
})
async def get_item_from_db(dialog_manager: DialogManager, **kwargs):
    item_id = int(dialog_manager.dialog_data.get("current_dish"))
    current_table = dialog_manager.dialog_data.get("current_table")
    current_schema = dialog_manager.dialog_data.get("current_schema")

    dish_information = await _get_item_by_id(
        schema_name=current_schema,
        table_name=current_table,
        item_id=item_id
    )

    # print(dish_information)
    if 'Item not found' in dish_information:
        return {
            "id": 0,
            "name": "",
            "description": "",
            "img": "",
            "price": 0.0,
            "type": "",
            "status": "❌Inactive"
        }

    product_inform_dict = {
        "id": dish_information["id"],
        "name": dish_information["name"],
        "description": dish_information["description"],
        "img": dish_information["img"],
        "price": dish_information["price"],
        "type": dish_information["type"],
        "status": "✅Active" if dish_information["status"] else "❌Inactive"
    }

    dialog_manager.dialog_data["````````````status_action````````````"] = ""
    dialog_manager.dialog_data["dish_information"] = product_inform_dict
    product_inform_dict["description"] = dish_information["description"][:10]

    image = MediaAttachment(
        ContentType.PHOTO, url=product_inform_dict.get("img"))

    return {"dish_information": product_inform_dict, "photo": image}


def fix_base64_padding(base64_string: str) -> str:
    missing_padding = len(base64_string) % 4
    if missing_padding:
        base64_string += "=" * (4 - missing_padding)
    return base64_string


@save_dialog_getter(default={
    "status_action": "unknown"
})
async def get_action(dialog_manager: DialogManager, **kwargs):

    status_action = dialog_manager.dialog_data.get("status_action", "")
    if status_action in ["✅Active", "❌Inactive"]:
        if "✅" in status_action:
            return {"status_action": "❌Block"}
        else:
            return {"status_action": "✅Unblock"}
    elif status_action == "img":
        dish_information = dialog_manager.dialog_data.get(
            "dish_information")
        img_url = dish_information.get("img")

        image = MediaAttachment(
            ContentType.PHOTO, url=img_url)
        return {"status_action": "img", "photo": image}

    return {"status_action": ""}


@save_dialog_getter(default={
    "cooks_list": [{
        "id": "unknown",
        "cook_name": "unknown",
        "level": "unknown",
        "level_emoji": "unknown",
        "status_text": "unknown"
    }]
})
async def get_all_cooks(dialog_manager: DialogManager, **kwargs):
    items = await _get_items_from_table_by_models(Cooks)

    dialog_manager.dialog_data["cooks_list"] = items
    return {"cooks_list": items}


@save_dialog_getter(default={
    "current_cook": {
        "id": "unknown",
        "cook_name": "unknown",
        "level": "unknown",
        "level_emoji": "unknown",
        "status_text": "unknown"
    }
})
async def get_current_cook(dialog_manager: DialogManager, **kwargs):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)

    cooks_list = dialog_manager.dialog_data.get("cooks_list")
    cook_telegram_id = int(dialog_manager.dialog_data.get("selected_cook"))

    cook = next((cook for cook in cooks_list if cook.telegram_id ==
                 cook_telegram_id), Cooks_l(0, "None", 0, 0, False))
    dialog_manager.dialog_data["current_cook"] = cook
    return {"current_cook": cook}


@save_dialog_getter(default={
    "status_action": "unknown"
})
def get_action_cook_window(dialog_manager: DialogManager, **kwargs):
    return {"status_action": dialog_manager.dialog_data.get("status_action")}


@save_dialog_getter(default={
    "status_action": "unknown"
})
async def get_admin_status(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    return {"sound_status": config.ADMIN_LIST.get(user_id)}


@save_dialog_getter(default={
    "today_orders": {
        "id": "unknown",
        "name": "unknown",
        "phone_number": "unknown",
        "email": "unknown",
        "items": "unknown",
        "total_amount": "unknown",
        "delivery_time": "unknown",
        "delivery_method": "unknown",
        "location": "unknown",
        "status": "unknown",
        "delivery_time": "unknown",
        "delivery_date": "unknown"
    }
})
async def get_orders_by_date(dialog_manager: DialogManager, **kwargs):
    orders = dialog_manager.start_data.get("orders", [])
    for order in orders:
        if not order.delivery_time:
            order.delivery_time = 'asap'
    return {"today_orders": orders}


@save_dialog_getter()
async def get_current_order(dialog_manager: DialogManager, **kwargs):

    order_status_next = {
        "pending": "Accept the order🟩",
        "processing": "Compleat✅",
        "ready to delivery": "Ready to delivery🔥"
    }

    current_order_id = dialog_manager.dialog_data.get("current_order_id")

    if not current_order_id:
        current_order_id = dialog_manager.start_data.get('order_id')

    order = await _get_items_from_table_by_models(
        Table=Orders,
        filter_column="id",
        filter_column_data=int(current_order_id)
    )

    order_items = []

    for index, item in enumerate(order[0].items):
        order_items.append({
            "id": item["id"],
            "index": index + 1,
            "table_name": item["table_name"],
            "name": item["name"],
            "q-w": item["quantity"] if item["type"] == "by portion" else item["weight"],
            "additions": item["additions"]
        })

    dialog_manager.dialog_data["current_order"] = order[0]

    return {"current_order": order[0], "order_items": order_items, "order_status_value": order_status_next.get(order[0].status)}


@save_dialog_getter()
async def get_order_warning_data(dialog_manager: DialogManager, **kwargs):
    orders = dialog_manager.start_data.get('warning_data')
    order_id = dialog_manager.start_data.get('order_id')
    dialog_manager.dialog_data.update(dialog_manager.start_data)
    return {'orders': orders}
