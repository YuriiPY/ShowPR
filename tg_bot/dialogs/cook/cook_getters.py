import asyncio
from aiogram import Bot
from datetime import datetime
from itertools import zip_longest
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram.enums import ContentType

from services.cook import CookServices
from db.crud.users.crud import (
    _get_cook_work_schedule,
    _get_item_by_id,
    _get_items_from_table,
    _get_tables_in_schema,
    _get_items_from_table_by_models
)
from core import config
from db.models.orders.orders import Orders
from dialogs.cook.cook_states import CookMenuSelection
from decorators.decorators import save_dialog_getter


@save_dialog_getter()
async def get_cook_inform(dialog_manager: DialogManager, **kwargs):
    cook = await CookServices.get_cook(dialog_manager.middleware_data.get("event_from_user").id)
    dialog_manager.dialog_data["cook_information"] = cook
    return {"cook_information": cook}


@save_dialog_getter()
async def get_order_handle_button(dialog_manager: DialogManager, **kwargs):
    print("HERE IT IS", dialog_manager.dialog_data["cook_information"])


@save_dialog_getter()
async def get_current_schedule(dialog_manager: DialogManager, **kwargs):
    schedule = await _get_cook_work_schedule(dialog_manager.dialog_data.get("cook_information").telegram_id)

    return {"cook_schedule": schedule}


@save_dialog_getter()
async def get_tables(dialog_manager: DialogManager, **kwargs):
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


@save_dialog_getter()
async def get_table_items(dialog_manager: DialogManager, **kwargs):
    current_table: str = dialog_manager.dialog_data.get("current_table")
    if (current_schema := dialog_manager.dialog_data.get("current_schema")) is None:
        current_schema: str = dialog_manager.start_data.get("current_schema")
        current_table: str = dialog_manager.start_data.get("current_table")
        dialog_manager.dialog_data.update(dialog_manager.start_data)

    menu_items = []

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


@save_dialog_getter()
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
        return {"dish_information":
                {
                    "id": 0,
                    "name": "",
                    "description": "",
                    "img": "",
                    "price": 0.0,
                    "type": "",
                    "status": "❌Inactive"
                }
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


@save_dialog_getter()
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


@save_dialog_getter()
async def get_orders_by_date(dialog_manager: DialogManager, **kwargs):
    orders = dialog_manager.start_data.get("orders", [])

    return {"today_orders": orders}


@save_dialog_getter()
async def get_current_order(dialog_manager: DialogManager, **kwargs):

    order_status_next = {
        "pending": "Accept the order🟩",
        "processing": "Compleat✅",
        "ready to delivery": "Ready to delivery🔥"
    }

    current_order_id = dialog_manager.dialog_data.get("current_order_id")

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
