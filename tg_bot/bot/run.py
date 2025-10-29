from datetime import datetime
from aiogram.fsm.storage.base import StorageKey
import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery, Update
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiogram_dialog.api.exceptions import NoContextError

import core.config as config
from bot.bot import dp, bot
from helpers.message import delayed_delete_message
from services.admin import AdminServices
from services.cook import CookServices
from dialogs.admin.admin_states import AdminMenuSelection, Admin_Order
from dialogs.cook.cook_states import CookMenuSelection, Cook_Order
from dialogs.admin.admin_dialogs import (
    main_admin_menu,
    confirm_server,
    server_dialog,
    menu_dialog,
    cooks_list_dialog,
    setting_dialog,
    admin_orders_dialog
)
from dialogs.cook.cook_dialogs import (
    main_cook_menu,
    work_dialog,
    cook_menu_dialog,
    cook_setting_dialog,
    cook_orders_dialog
)
from db.crud.users.crud import (
    _get_items_from_table_by_models,
    _get_item_by_telegram_id,
    _update_user_data_by_telegram_id
)
from db.models.orders.orders import Orders
from db.models.users.admin import Admin
from db.models.users.cook import Cooks
from handlers.errors.error_handler import error_router

main_router = Router()

dp.include_routers(main_admin_menu, menu_dialog,
                   server_dialog, confirm_server,
                   admin_orders_dialog, cooks_list_dialog,
                   setting_dialog, main_cook_menu,
                   work_dialog, cook_menu_dialog,
                   cook_setting_dialog, cook_orders_dialog,
                   error_router
                   )
setup_dialogs(dp)


class Registration(StatesGroup):
    answer = State()
    role = State()
    confirm_role = State()

    admin = State()
    cook = State()

    cook_work_day_start = State()


accept_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Yes'), KeyboardButton(text='No')]
], resize_keyboard=True, input_field_placeholder='Choose the answer')

role_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='admin'), KeyboardButton(
        text='cook'), KeyboardButton(text='user')]
], resize_keyboard=True, input_field_placeholder='Choose the answer')


@dp.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext, dialog_manager: DialogManager):
    user_id = message.from_user.id

    if (admin_information := await AdminServices.get_admin(user_id)) is not None:
        if not admin_information.logged_in:
            msg = await message.answer(f'Hi {admin_information.admin_name} please enter your password to log in:')

            await state.update_data({
                'admin_is_logged_in': True,
                'logged_msg_to_delete': msg
            })
            await state.set_state(Registration.admin)

            return

        config.ADMIN_LIST[user_id] = admin_information

        await dialog_manager.start(AdminMenuSelection.main_menu, mode=StartMode.RESET_STACK)

    elif (cook_information := await CookServices.get_cook(user_id)) is not None:

        if not cook_information.logged_in:
            msg = await message.answer(f'Hi {cook_information.cook_name} please enter your password to log in:')

            await state.update_data({
                'cook_is_logged_in': True,
                'logged_msg_to_delete': msg
            })
            await state.set_state(Registration.cook)

            return

        config.COOKS_LIST[user_id] = cook_information

        await dialog_manager.start(CookMenuSelection.main_menu, mode=StartMode.RESET_STACK)

    else:
        await message.answer("I did`t see u before, do u wanna register here?", reply_markup=accept_keyboard)
        await state.set_state(Registration.answer)


@dp.message(Registration.answer)
async def first_registration_answer(message: Message, state: FSMContext):
    if message.text == "Yes":
        await state.set_state(Registration.role)
        await message.answer("Who are u?", reply_markup=role_keyboard)

    else:
        await message.answer("bye", reply_markup=ReplyKeyboardRemove())
        await state.clear()


@dp.message(Registration.role)
async def second_registration_answer(message: Message, state: FSMContext):
    if message.text == "admin":
        await message.answer("Enter password:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.admin)

    elif message.text == "cook":
        await message.answer("Enter password:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.cook)

    else:
        await message.answer("Enjoy our food ❤️", reply_markup=ReplyKeyboardRemove())


@dp.message(Registration.admin)
async def third_registration_answer(
    message: Message,
    state: FSMContext,
    dialog_manager: DialogManager
):
    state_data = await state.get_data()
    attempts_left = state_data.get("attempts", 3)

    if message.text == config.PASSWORD_ADMIN:

        admin_name = message.from_user.first_name
        admin_telegram_id = message.from_user.id
        admin_is_logged_in = state_data.get('admin_is_logged_in')

        if admin_is_logged_in:
            response_msg = state_data.get('logged_msg_to_delete')
            if response_msg:
                await response_msg.delete()

            result = await _update_user_data_by_telegram_id(
                user_table=Admin,
                telegram_id=admin_telegram_id,
                item_data={
                    'logged_in': True
                }
            )

            msg = await message.answer("Role ADMIN confirmed✅")
            asyncio.create_task(delayed_delete_message(msg, 2))

            config.ADMIN_LIST[admin_telegram_id] = result.get('user')
            await state.clear()
            await dialog_manager.start(AdminMenuSelection.main_menu, mode=StartMode.RESET_STACK)

        elif new_admin := await AdminServices.set_new_admin(admin_name, admin_telegram_id, 1):
            response_msg = await message.answer("Role ADMIN confirmed✅")
            asyncio.create_task(delayed_delete_message(response_msg, 2))

            config.ADMIN_LIST[admin_telegram_id] = new_admin
            await state.clear()
            await dialog_manager.start(AdminMenuSelection.main_menu, mode=StartMode.RESET_STACK)

        else:
            await state.clear()
            msg = await message.answer("Something wrong with database")
            asyncio.create_task(delayed_delete_message(msg, 2))

    else:
        attempts_left -= 1
        if attempts_left > 0:
            await state.update_data(attempts=attempts_left)
            await message.answer(f"Incorrect password. You have {attempts_left} attempt(s). Please try again:")
        else:
            await state.clear()
            await message.answer("Sorry, you have used all of your attempts. Registration failed ❌")


@dp.message(Registration.cook)
async def third_registration_answer(
    message: Message,
    state: FSMContext,
    dialog_manager: DialogManager
):
    state_data = await state.get_data()
    attempts_left = state_data.get("attempts", 3)

    if message.text == config.PASSWORD_COOK:

        cook_name = message.from_user.first_name
        cook_telegram_id = message.from_user.id
        cook_is_logged_in = state_data.get('cook_is_logged_in')

        if cook_is_logged_in:
            response_msg = state_data.get('logged_msg_to_delete')
            if response_msg:
                await response_msg.delete()

            result = await _update_user_data_by_telegram_id(
                user_table=Cooks,
                telegram_id=cook_telegram_id,
                item_data={
                    'logged_in': True
                }
            )

            response_msg = await message.answer("Role ADMIN confirmed✅")
            asyncio.create_task(delayed_delete_message(response_msg, 2))

            config.ADMIN_LIST[cook_telegram_id] = result.get('user')
            await state.clear()
            await dialog_manager.start(AdminMenuSelection.main_menu, mode=StartMode.RESET_STACK)

        elif new_cook := await CookServices.set_new_cook(cook_name, cook_telegram_id, 1):
            response_msg = await message.answer("Role COOK confirmed✅")
            asyncio.create_task(delayed_delete_message(response_msg, 2))

            config.ADMIN_LIST[cook_telegram_id] = new_cook
            await state.clear()
            await dialog_manager.start(CookMenuSelection.main_menu, mode=StartMode.RESET_STACK)

        else:
            await state.clear()
            msg = await message.answer("Something wrong with database")
            asyncio.create_task(delayed_delete_message(msg, 2))
    else:
        attempts_left -= 1
        if attempts_left > 0:
            await state.update_data(attempts=attempts_left)
            await message.answer(f"Incorrect password. You have {attempts_left} attempt(s). Please try again:")

        else:
            await state.clear()
            await message.answer("Sorry, you have used all of your attempts. Registration failed ❌")


@dp.callback_query(F.data == "show orders")
async def send_orders(
    callback_query: CallbackQuery,
    dialog_manager: DialogManager
):

    try:

        try:
            await dialog_manager.done()
        except NoContextError:
            pass
        except Exception as e:
            print(str(e))

        await callback_query.message.delete()

        user_id = callback_query.from_user.id

        current_date = datetime.now().date()

        orders = await _get_items_from_table_by_models(
            Table=Orders,
            order_by=["delivery_time"],
            filter_column="delivery_date",
            filter_column_data=current_date
        )
        cook = await _get_item_by_telegram_id(
            schema_name="team",
            table_name="cooks",
            telegram_id=user_id
        )
        admin = await _get_item_by_telegram_id(
            schema_name="team",
            table_name="admins",
            telegram_id=user_id
        )

        if orders:
            if cook != 'Item not found':
                await dialog_manager.start(state=Cook_Order.main_window, mode=StartMode.NORMAL, data={
                    "orders": orders
                })
            elif admin != 'Item not found':
                await dialog_manager.start(state=Admin_Order.main_window, mode=StartMode.NORMAL, data={
                    "orders": orders
                })

        else:
            sended_message = await callback_query.message.answer("No orders today yet")
            asyncio.create_task(delayed_delete_message(sended_message, 2))

    except Exception as e:
        print(str(e))

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())
