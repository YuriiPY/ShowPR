import datetime
from sqlalchemy import select
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram.fsm.state import State

from geopy.distance import geodesic
import asyncio

from core.config import ADMIN_LIST, COOKS_LIST
from db.crud.users.crud import (
    _update_item_data,
    _update_user_data_by_telegram_id,
    _create_table_item
)
from db.session import async_session_maker
from db.models.users.cook import Cooks
from db.models.work_schedule.work_schedule import WorkSchedule
from db.crud.users.crud import handle_exception


class CookServices:

    @staticmethod
    @handle_exception
    async def get_cook(telegram_id: int) -> Cooks:
        async with async_session_maker() as session:
            stmt = select(Cooks).where(Cooks.telegram_id == telegram_id)
            is_exist = await session.execute(stmt)
            cook = is_exist.scalars().first()
            return cook

    @staticmethod
    @handle_exception
    async def set_new_cook(name: str, telegram_id: int, level: int):
        async with async_session_maker() as session:
            new_cook = Cooks(
                cook_name=name,
                telegram_id=telegram_id,
                level=level,
                status=False
            )
            session.add(new_cook)
            await session.flush()
            await session.refresh(new_cook)
            await session.commit()

            return new_cook

    @staticmethod
    @handle_exception
    async def handle_work_status(telegram_id: int, status: bool):
        async with async_session_maker() as session:
            result = await _update_item_data(
                schema_name="team",
                table_name="cooks",
                item_id=telegram_id,
                item_data=status,
                item_column="status",
                query_param="telegram_id"
            )

            if result.get("func_status") == "Item was updated✅":
                return "Nice to see you at work"
            else:
                return "Can`t start your work day!"

    @staticmethod
    async def check_cook_location(lat, lon):
        first_location = (51.12100248921536, 17.044551076763636)
        second_location = (51.116116346557654, 17.0059383686113)
        distance1 = geodesic(first_location, (lat, lon)).meters
        distance2 = geodesic(second_location, (lat, lon)).meters

        if distance1 <= 500 or distance2 <= 500:
            return True
        return False

    @staticmethod
    @handle_exception
    async def handle_cook_day(telegram_id: int, work_status: bool):

        today = datetime.date.today()

        print("TODAY ->", today)

        if work_status:

            result_create = await _create_table_item(WorkSchedule, {
                "telegram_id": telegram_id,
                "work_date": today,
                "start_time": datetime.datetime.now().time().replace(microsecond=0)
            })
            print(result_create)

            if "✅" in result_create.get("func_status"):
                result_update = await _update_user_data_by_telegram_id(Cooks, telegram_id, {"status": True})

                return {"func_status": "Your workday is started✅"}

            return False

        else:

            result_create = await _update_user_data_by_telegram_id(
                WorkSchedule,
                telegram_id,
                {
                    "end_time": datetime.datetime.now().time().replace(microsecond=0)
                },
                additional_filters={
                    WorkSchedule.work_date: today
                }

            )

            print(result_create)

            if "✅" in result_create.get("func_status"):
                result_update = await _update_user_data_by_telegram_id(Cooks, telegram_id, {"status": False})
                print(result_update)

                return {"func_status": "Your workday is finished✅"}

            return False

    @staticmethod
    @handle_exception
    async def cook_level_check(
        Callback_query: CallbackQuery,
        dialog_manager: DialogManager,
        next_state: State,
        access_level: int
    ):
        cook = await CookServices.get_cook(dialog_manager.middleware_data.get("event_from_user").id)

        if cook.level < access_level:
            send_message = await Callback_query.message.answer("Access denied❌")
            await asyncio.sleep(2)
            await send_message.delete()
            await dialog_manager.start(next_state, mode=StartMode.RESET_STACK)

            return True
        else:
            return False
