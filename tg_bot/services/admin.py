import logging
import asyncio
import httpx
from urllib.parse import urljoin
from typing import Union
from sqlalchemy import select
from datetime import datetime, timedelta
from aiogram import Bot
from aiogram_dialog import DialogManager

from core.config import CURRENT_SERVER_STATUS, ADMIN_LIST, COOKS_LIST, BACKEND_URL
from db.session import async_session_maker
from db.models.users.admin import Admin
from db.crud.users.crud import _update_item_data
from db.crud.users.crud import handle_exception
from core.config import BACKEND_ADMIN_NAME, BACKEND_ADMIN_PASSWORD


logging.basicConfig(level=logging.INFO)


class AdminServices:

    @staticmethod
    @handle_exception
    async def get_admin(telegram_id: int) -> Admin:
        async with async_session_maker() as session:
            stmt = select(Admin).where(Admin.telegram_id == telegram_id)
            is_exist = await session.execute(stmt)
            admin = is_exist.scalars().first()
            return admin

    @staticmethod
    @handle_exception
    async def set_new_admin(name: str, telegram_id: int, level: int):
        async with async_session_maker() as session:
            new_admin = Admin(
                admin_name=name,
                telegram_id=telegram_id,
                level=level,
                status=True
            )
            session.add(new_admin)
            await session.flush()
            await session.refresh(new_admin)
            await session.commit()

            return new_admin

    @staticmethod
    @handle_exception
    async def close_store(time: Union[None, str] = None):
        print(time, type(time))

        auth = (
            BACKEND_ADMIN_NAME, BACKEND_ADMIN_PASSWORD
        )

        request_data = {
            "until": None,
            "close_now": None
        }

        if time == "CL_BE_OP":
            request_data["close_now"] = True

        elif isinstance(time, str):
            request_data["until"] = time

        elif len(time) == 2:
            request_data["until"] = time + ":00"

        else:
            return {"func_status": "Something wrong"}

        async with httpx.AsyncClient() as client:
            print('client')
            url = urljoin(BACKEND_URL, f'store/close')
            response = await client.post(
                url=url,
                json=request_data,
                auth=auth
            )
            print('request')

            if response.status_code == 200:
                CURRENT_SERVER_STATUS["status"] = time
                data = response.json()
                # logging.info("%s %s %s", admin_name,
                #              message, CURRENT_SERVER_STATUS)
                return {"func_status": f"The store {data.get('message')}"}
            else:
                error_text = response.text
                return {f"func_status": f"Something wrong with server connection {error_text}"}

    @staticmethod
    @handle_exception
    async def open_store(*args, **kwargs):

        auth = (
            BACKEND_ADMIN_NAME, BACKEND_ADMIN_PASSWORD
        )

        async with httpx.AsyncClient() as client:
            print('client')
            url = urljoin(BACKEND_URL, f'store/open')
            print("BACK END URL BEFORE OPEN THE STORE", url)
            response = await client.post(
                url=url,
                auth=auth
            )
            print('request')

            if response.status_code == 200:
                CURRENT_SERVER_STATUS["status"] = "open"
                # logging.info("%s %s", admin_name, CURRENT_SERVER_STATUS)
                return {"func_status": f"The store is opened"}
            else:
                error_text = response.text()
                return {f"func_status": f"Something wrong with server connection {error_text}"}

    @staticmethod
    async def send_message_to_cook(dialog_manager: DialogManager, user_id: int, message_text: str):
        bot: Bot = dialog_manager.middleware_data['bot']
        await bot.send_message(chat_id=user_id, text=message_text, disable_notification=False)
        print(f"Send a message to {user_id}, {message_text}")

    @staticmethod
    @handle_exception
    async def change_level_status(table_name: str, user_telegram_id: int, new_level: int):
        result = await _update_item_data(
            schema_name="team",
            table_name=table_name,
            item_id=user_telegram_id,
            item_data=new_level,
            item_column="level",
            query_param="telegram_id"
        )
        return result

    @staticmethod
    @handle_exception
    async def create_new_item_in_db(table: str, item_fields: dict):

        auth = (
            BACKEND_ADMIN_PASSWORD, BACKEND_ADMIN_PASSWORD
        )

        async with httpx.AsyncClient() as client:
            print('client')
            url = urljoin(BACKEND_URL, f'products/create/{table}')
            response = await client.post(
                url,
                json=item_fields,
                auth=auth
            )
            print('request')

            if response.status_code == 200:
                new_item = response.json()
                print(new_item)
                return {"func_status": "Product successfully created!", "new_item": new_item}
            else:
                print(response.text)
                return {"func_status": 'Failed to create a new item', 'detail': response.text, "new_item": None}


item_fields = {
    "name": "Newwwwwwwww Item",
    "price": 100,
    "type": "by weight",
    "status": True,
    "img": "buiygbaervyuilegbfue3febughfkebhugb",
    "description": "A new electronic item"
}

# asyncio.run(AdminServices.create_new_item_in_db("soups", item_fields))
