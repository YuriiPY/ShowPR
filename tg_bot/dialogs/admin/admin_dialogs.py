from itertools import zip_longest
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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
    Group
)
from aiogram.utils.formatting import Bold
from aiogram_dialog.widgets.text import Const, Format, Multi, Text
from addons.CustomScrollingGroup import CustomScrollingGroup
from typing import Callable

from dialogs.admin.admin_states import (
    Admin_Confirm,
    AdminMenuSelection,
    Server,
    Admin_Menu,
    Cooks,
    Admin_Settings,
    Admin_Order
)
from dialogs.admin.admin_getters import *
from dialogs.admin.admin_callbacks import *
from services.admin import AdminServices


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
        state=Admin_Confirm.Confirm,
    )
)

main_admin_menu = Dialog(
    Window(
        Multi(
            Const("Your current menu:"),
            sep='\n',
        ),
        Start(
            Const("Server🖥"),
            id="Server",
            state=Server.Server,
        ),
        Start(
            Const("Menu🧾"),
            id="menu",
            state=Admin_Menu.menu,
        ),
        Button(
            Const("Orders🧧"),
            id="order",
            on_click=open_orders,
        ),
        Start(
            Const("Cooks🧑🏻‍🍳"),
            id="cooks",
            state=Cooks.cooks_list,
        ),
        Start(
            Const("Texts💬"),
            id="gpt",
            state=AdminMenuSelection.Texts,
        ),
        Start(
            Const("Settings⚙️"),
            id="settings",
            state=Admin_Settings.main_settings,
        ),
        state=AdminMenuSelection.main_menu,
    ),
)
server_dialog = Dialog(
    Window(
        Multi(
            Const("Server settings"),
            Format("Status server:{server_status}"),
            Format("Status store:{store_status}"),
        ),
        Column(
            Button(
                Const("Open store"),
                id="open_store",
                on_click=lambda callback_query, Button, dialog_manager:
                store_click(
                    callback_query=callback_query,
                    dialog_manager=dialog_manager,
                    widget_id=Button.widget_id,
                    action=AdminServices.open_store,
                    kwargs={}
                ),
                when=lambda data, widget, manager: not data.get(
                    "dialog_data").get("store_status"),
            ),
            Start(
                Const("Close store"),
                id="close_store",
                state=Server.Selection_close_time,
                when=lambda data, widget, manager: data.get(
                    "dialog_data").get("store_status"),
            ),
            id="server_settings",
        ),
        Button(
            Const("⬅️Back"),
            id="getBack",
            on_click=get_back_dialog,
        ),
        state=Server.Server,
        getter=(checking_server_status, get_admin_data)
    ),
    Window(
        Const("Choose/Write close time:"),
        TextInput(
            id="close_time_input",
            on_success=lambda event, widget, dialog_manager, state:
                store_click(
                    callback_query=event,
                    dialog_manager=dialog_manager,
                    widget_id="close_server",
                    action=AdminServices.close_store,
                    kwargs={"time": event.text}
                ),
        ),
        Column(
            Select(
                Format("{item.show_text}"),
                id="close_time_selector",
                items="time_slots",
                item_id_getter=lambda item: item.time,
                on_click=lambda event, source,  dialog_manager, item_id:
                store_click(
                    callback_query=event,
                    dialog_manager=dialog_manager,
                    widget_id="close_store",
                    action=AdminServices.close_store,
                    kwargs={"time": item_id}
                )
            ),
        ),
        Back(Const("⬅️Back")),
        getter=get_possible_close_time,
        state=Server.Selection_close_time,
    ),
    # ADD WINDOW FOR START AND STOP SERVER LOVE YOU <З
)

menu_dialog = Dialog(
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
        state=Admin_Menu.menu,
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
        state=Admin_Menu.delicious_menu,
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
        state=Admin_Menu.current_dish_menu,
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
        state=Admin_Menu.last_menu_window,
        getter=get_action
    ),
    # TODO: MAKE FUNCTION FOR CREATING A NEW ITEM FOR DB / CREATE A NEW ITEM USING ONLY BOT/ CREATE FUNCTION FOR CREATE MANY-ITEMS✅Active"), KeyboardButton(text="❌Inactive
    Window(
        Format("{dialog_data[action]}"),
        Format(
            "{dialog_data[error_value]}",
            when=lambda data, widget, dialog_manager: data.get(
                "dialog_data").get("error_value") is not None
        ),
        Row(
            Button(
                Const("by portion"),
                id="by_portion",
                on_click=lambda callback_query, widget, dialog_manager: handle_input_for_create(
                    callback_query,
                    widget,
                    dialog_manager,
                    "by portion"
                )
            ),
            Button(
                Const("by weight"),
                id="by_weight",
                on_click=lambda callback_query, widget, dialog_manager: handle_input_for_create(
                    callback_query,
                    widget,
                    dialog_manager,
                    "by weight"
                )
            ),
            when=lambda data, *
            args, **kwargs: data['dialog_data']['action'] == 'Select product type:'
        ),
        Row(
            Button(
                Const("✅Active"),
                id="active_status",
                on_click=lambda callback_query, widget, dialog_manager: handle_input_for_create(
                    callback_query,
                    widget,
                    dialog_manager,
                    "✅Active"
                )
            ),
            Button(
                Const("❌Inactive"),
                id="inactive_status",
                on_click=lambda callback_query, widget, dialog_manager: handle_input_for_create(
                    callback_query,
                    widget,
                    dialog_manager,
                    "❌Inactive"
                )
            ),
            when=lambda data, *
            args, **kwargs: data['dialog_data']['action'] == 'Select product status:'
        ),
        MessageInput(handle_input_for_create),
        state=Admin_Menu.add_new_dish_menu
    )
)

cooks_list_dialog = Dialog(
    Window(
        Format("Pierogowa cooks:"),
        Group(
            Select(
                Format(
                    """{item.id} {item.cook_name}
                    {item.level}{item.level_emoji} {item.status_text}"""),
                id="cooks",
                items="cooks_list",
                item_id_getter=lambda item: item.telegram_id,
                on_click=selected_cook,
            ),
            id="cooks_list",
            width=1,
        ),
        Button(
            Const("⬅️Back"),
            id="getBack",
            on_click=get_back_dialog,
        ),
        state=Cooks.cooks_list,
        getter=get_all_cooks,
    ),
    Window(
        Format("{current_cook.cook_name}"),
        Button(
            Format("Write a message📝"),
            id="write_to_cook_btn",
            on_click=lambda Callback_query, widget, dialog_manager: current_cook_btn(
                Callback_query=Callback_query,
                widget=widget,
                dialog_manager=dialog_manager,
                current_action="write",
            ),
        ),
        Button(
            Format("Working hours⏳"),
            id="hours_cook_btn",
        ),
        Button(
            Format("Level {current_cook.level}{current_cook.level_emoji}"),
            id="level_cook_btn",
            on_click=lambda Callback_query, widget, dialog_manager: current_cook_btn(
                Callback_query=Callback_query,
                widget=widget,
                dialog_manager=dialog_manager,
                current_action="level",
            ),
        ),
        Button(
            Format("Status {current_cook.status_text}"),
            id="status_cook_btn",
        ),
        Back(Const("⬅️Back")),
        state=Cooks.current_cook,
        getter=get_current_cook,
    ),
    Window(
        Format("status"),
        TextInput(
            id="cook_input",
            type_factory=str,
            on_success=write_message,
            on_error=incorrectly_written_data,
        ),
        Group(
            Button(
                Const("🥇"),
                id="cook_level_btn_1",
                on_click=lambda Callback_query, widget, dialog_manager: change_level(
                    Callback_query=Callback_query,
                    widget=widget,
                    dialog_manager=dialog_manager,
                    new_level=1,
                ),
            ),
            Button(
                Const("🥈"),
                id="cook_level_btn_2",
                on_click=lambda Callback_query, widget, dialog_manager: change_level(
                    Callback_query=Callback_query,
                    widget=widget,
                    dialog_manager=dialog_manager,
                    new_level=2,
                ),
            ),
            Button(
                Const("🥉"),
                id="cook_level_btn_3",
                on_click=lambda Callback_query, widget, dialog_manager: change_level(
                    Callback_query=Callback_query,
                    widget=widget,
                    dialog_manager=dialog_manager,
                    new_level=3,
                ),
            ),
            when=lambda dialog_manager, *
            args, **kwargs: "level" in dialog_manager.get("dialog_data").get("status_action"),
            width=3,
        ),
        Back(Const("⬅️Back")),
        # getter=get_action_cook_window,
        state=Cooks.last_cook_window,
    ),
)


admin_orders_dialog = Dialog(
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
        state=Admin_Order.main_window
    ),
    Window(
        Format(
            "Client name: {current_order.name} \nPhone number: {current_order.phone_number} \nEmail: {current_order.email}"),
        Format(
            "\nLocation: \nStreet: {current_order.location[street]} \nHome: {current_order.location[home]} \nHome number: {current_order.location[homeNumber]}"
        ),
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
            on_click=handle_order_status
        ),
        Button(
            Const("⬅️Back"),
            id="getBack",
            on_click=open_orders,
        ),
        getter=get_current_order,
        state=Admin_Order.current_order
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
        state=Admin_Order.current_dish_information,
        getter=get_item_from_db,
    ),
    Window(
        Format("New order:\n {orders}"),
        Button(
            Const('Show order'),
            id='show_order',
            on_click=show_new_order
        ),
        state=Admin_Order.warning_window,
        getter=get_order_warning_data)
)


setting_dialog = Dialog(
    Window(
        Const("Settings"),
        Button(
            Format(""),  # turn off/on sound of bot,
            id="sound_btn",
        ),
        Button(
            Const("Log out🔑"),
            id="log_out",
            on_click=log_out
        ),
        Cancel(Const("⬅️Back")),
        state=Admin_Settings.main_settings,
    )
)
