from aiogram_dialog import Data, Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
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
    Group,
    SwitchTo
)
from aiogram_dialog.widgets.text import Const, Format, Multi, Text
from addons.CustomScrollingGroup import CustomScrollingGroup

from dialogs.cook.cook_states import *
from dialogs.cook.cook_getters import *
from dialogs.cook.cook_callbacks import *

confirm_server = Dialog(
    Window(
        Format("Please confirm: {start_data[action_name]}"),
        Row(
            Button(
                Const("✅Confirm"),
                id="confirm",
                on_click=lambda callback_query, Button, dialog_manager: confirm_action(
                    callback_query=callback_query, dialog_manager=dialog_manager),
            ),
            Button(
                Const("❌Cancel"),
                id="cancel",
                on_click=lambda callback_query, Button, dialog_manager: cancel_action(
                    callback_query=callback_query, dialog_manager=dialog_manager),
            ),
        ),
        state=Cook_Confirm.Confirm,
    )
)


main_cook_menu = Dialog(
    Window(
        Multi(
            Const("Your current menu:"),
            sep='\n',
        ),
        Button(
            Const("Orders🧧"),
            id="order",
            on_click=open_orders,
        ),
        Start(
            Const("Work💼"),
            id="work",
            state=Work.main_work
        ),
        Start(
            Const("Menu🧾"),
            id="menu",
            state=Cook_Menu.menu,
            when=lambda data, widget, manager: data["cook_information"].level >= 1
        ),
        Start(
            Const("Server🖥"),
            id="Server",
            state=CookMenuSelection.Texts,
            when=lambda data, widget, manager: data["cook_information"].level >= 1
        ),
        Start(
            Const("Settings⚙️"),
            id="settings",
            state=Cook_Settings.main_settings,
        ),
        getter=get_cook_inform,
        state=CookMenuSelection.main_menu
    )
)


async def get_keyboard(**kwargs):
    return {"reply_markup": location_keyboard}


work_dialog = Dialog(
    Window(
        Const(
            "Work menu:"
        ),
        Button(
            Const("Start work day🟩"),
            id="start_day",
            when=lambda data, widget, manager:
                data["cook_information"].status == False,
            on_click=send_verification,
            # state=Work.confirm_start_work
        ),
        Button(
            Const("Finish work day🟥"),
            id="finish_day",
            on_click=finish_working_day,
            when=lambda data, widget, manager:
                data["cook_information"].status == True
        ),
        SwitchTo(
            Const("Your working hours🕗"),
            id="working_hours",
            state=Work.work_hours
        ),
        Button(
            Const("⬅️Back"),
            id="getBack",
            on_click=get_back_dialog,
        ),
        getter=get_cook_inform,
        state=Work.main_work
    ),
    Window(
        Const("Working hours:"),
        CustomScrollingGroup(
            Select(
                Format(
                    "{item.work_date} | 🟩 {item.start_time} | 🟥 {item.end_time}"
                ),
                id="schedule",
                items="cook_schedule",
                item_id_getter=lambda item: item.id,
            ),
            id="cook_schedule",
            width=1,
            height=5
        ),
        Back(
            Const("⬅️Back"),
            id="getBack",
        ),
        getter=get_current_schedule,
        state=Work.work_hours
    ),
    Window(
        Const("Loc"),
        # MessageInput(
        #     func=handle_cook_location,
        #     content_types=["location"]
        # ),
        getter=get_keyboard,
        state=Work.confirm_start_work
    )
)


cook_menu_dialog = Dialog(
    Window(
        Const("Menu:"),
        Group(
            Button(
                Const("Cooked🔥"),
                id="cooked"
            ),
            Button(
                Const("Frozen❄️"),
                id="frozen"
            ),
            width=2
        ),
        Group(
            Select(
                Format("{item[button_name]}"),
                id="menu2",
                items="menu_buttons",
                item_id_getter=lambda item: f"{item['schema']}:{item['button_name']}",
                on_click=selected_menu_item,
            ),
            width=2,
        ),
        Button(
            Const("⬅️Back"),
            id="getBack",
            on_click=get_back_dialog,
        ),
        state=Cook_Menu.menu,
        getter=get_tables,
    ),
    Window(
        Const("Menu:"),
        CustomScrollingGroup(
            Select(
                Format(
                    "{item[index]:<1} {item[item_name]:<20} {item[active]:>7}"),
                id="menu3",
                items="menu_items",
                item_id_getter=lambda item: item['id'],
                on_click=selected_dish,
            ),
            id="custom_menu",
            width=1,
            height=7,
        ),
        Back(Const("⬅️Back")),
        state=Cook_Menu.delicious_menu,
        getter=get_table_items
    ),
    Window(
        Format("{dish_information[id]}"),
        DynamicMedia("photo"),
        Button(
            Format("Name: {dish_information[name]}"),
            id="name",
            on_click=lambda callback_query, widget, dialog_manager: current_dish_button(
                callback_query, widget, dialog_manager, "name"
            ),
        ),
        Button(
            Format("Price: {dish_information[price]}"),
            id="price",
            on_click=lambda callback_query, widget, dialog_manager: current_dish_button(
                callback_query, widget, dialog_manager, "price"
            ),
        ),
        Button(
            Format("Description: {dish_information[description]}..."),
            id="description",
            on_click=lambda callback_query, widget, dialog_manager: current_dish_button(
                callback_query, widget, dialog_manager, "description"
            ),
        ),
        Button(
            Format("Status: {dish_information[status]}"),
            id="status",
            on_click=lambda callback_query, widget, dialog_manager: current_dish_button(
                callback_query, widget, dialog_manager, "status"
            ),
        ),
        Button(
            Format("Image:"),
            id="photo",
            on_click=lambda callback_query, widget, dialog_manager: current_dish_button(
                callback_query, widget, dialog_manager, "img"
            ),
        ),
        Button(
            Format("❌Delete:"),
            id="delete",
            on_click=delete_button,
        ),
        Back(Const("⬅️Back")),
        state=Cook_Menu.current_dish_menu,
        getter=get_item_from_db,
    ),
    Window(
        Format("{dialog_data[action]}"),
        MessageInput(
            func=change_data_item
        ),
        Button(
            Format("{status_action}"),
            id="change_status",
            when=lambda data, *args, **kwargs: bool(data.get("status_action")),
            on_click=change_status_item,
        ),
        DynamicMedia(
            "photo",
            when=lambda data, widget, manager: data.get("dialog_data").get("status_action") == "img"),
        Back(Const("⬅️Back")),
        state=Cook_Menu.last_menu_window,
        getter=get_action
    )
)

cook_setting_dialog = Dialog(
    Window(
        Const("Settings"),
        Button(
            Format(""),  # TODO: turn off/on sound of bot,
            id="sound_btn",
        ),
        Button(
            Const("Log out🔑"),
            id="log_out",
            on_click=log_out
        ),
        Cancel(Const("⬅️Back")),
        state=Cook_Settings.main_settings,
    )
)


cook_orders_dialog = Dialog(
    Window(
        Format("Today`s orders ({today_orders[0].delivery_date}):"),
        CustomScrollingGroup(
            Select(
                Format(
                    "{item.delivery_time} | {item.items_length} Product(s) | {item.status}"),
                id="orders",
                items="today_orders",
                item_id_getter=lambda item: item.id,
                on_click=selected_order,
            ),
            id="custom_menu",
            width=1,
            height=7,
        ),
        Button(
            Const("⬅️Back"),
            id="getBack",
            on_click=get_back_dialog,
        ),
        getter=get_orders_by_date,
        state=Cook_Order.main_window
    ),
    Window(
        Format(
            "Client name: {current_order.name} \nPhone number: {current_order.phone_number} \nEmail: {current_order.email}"),
        Format("\nLocation: \nStreet: {current_order.location[street]} \nHome: {current_order.location[home]} \nHome number: {current_order.location[homeNumber]}",
               when=lambda data, widget, manager: data["cook_information"].level > 2),
        Group(
            Select(
                Format(
                    "{item[index]} | {item[table_name]} | {item[name]} | {item[q-w]} | {item[additions]}"),
                id="order_items",
                items="order_items",
                item_id_getter=lambda item: item['index'],
                on_click=selected_order_product,
            ),
            id="order_list",
            width=1,
        ),
        Button(
            Format("{order_status_value}"),
            id="accept_order",
            on_click=handle_order_status,
            # TODO:  Create a function for check cooks level
            when=lambda data, widget, manager: data["cook_information"].level > 2
        ),
        Back(Const("⬅️Back")),
        getter=(get_current_order, get_cook_inform),
        state=Cook_Order.current_order
    ),
    Window(
        Format("{dish_information[id]}"),
        DynamicMedia("photo"),
        Button(
            Format("Name: {dish_information[name]}"),
            id="name"
        ),
        Button(
            Format("Price: {dish_information[price]}"),
            id="price"
        ),
        Button(
            Format("Description: {dish_information[description]}..."),
            id="description"
        ),
        Button(
            Format("Status: {dish_information[status]}"),
            id="status"
        ),
        Back(Const("⬅️Back")),
        state=Cook_Order.current_dish_information,
        getter=get_item_from_db,
    ),
)
