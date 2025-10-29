import asyncio
from typing import Union
from sqlalchemy import and_, select, text, asc, desc
from functools import wraps

from db.session import async_session_maker
from db.base import Base
from db.models.users.cook import Cooks
from db.models.orders.orders import Orders
from db.models.work_schedule.work_schedule import WorkSchedule


def handle_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f'❌ Error in {func.__name__}: {e}')

    return wrapper


@handle_exception
async def _create_table_item(
        user_table: Base,
        item_data: dict
):
    async with async_session_maker() as session:
        try:
            session.add(user_table(**item_data))
            print("Item was successfully created✅")

            await session.commit()
            return {"func_status": "Item was successfully created✅"}
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {str(e)}")
            return {"func_status": f"❌ Error: {str(e)}"}


@handle_exception
async def _get_tables_in_schema(schema: str) -> tuple:
    async with async_session_maker() as session:
        query = text(
            f"SELECT * FROM pg_catalog.pg_tables WHERE schemaname='{schema}'")
        result = await session.execute(query, {"schema": schema})

        tables = [row[1] for row in result.fetchall()]
        return (schema, tables)


@handle_exception
async def _get_items_from_table_by_models(
        Table: Base,
        order_by: list[str] = ["id"],
        filter_column: Union[str, None] = None,
        filter_column_data: Union[any, None] = None,
        descending: bool = False
) -> list[Base]:
    async with async_session_maker() as session:

        order_columns = [
            desc(getattr(Table, column, Table.id)) if descending
            else asc(
                getattr(Table, column, Table.id))
            for column in order_by
        ]

        if filter_column:
            filter_data = getattr(Table, filter_column)
            result = await session.execute(select(Table).where(filter_data == filter_column_data).order_by(*order_columns))
        else:
            result = await session.execute(select(Table).order_by
                                           (*order_columns))

        items = result.scalars().all()
        return items


@handle_exception
async def _get_items_from_table(schema_name: str, table_name: str, columns: list):
    columns = ", ".join(columns)
    async with async_session_maker() as session:
        query = text(
            f"SELECT {columns} FROM {schema_name}.{table_name} ORDER BY id ASC"
        )

        result = await session.execute(query)
        rows = result.fetchall()
        print(rows, type(rows))
        return rows


@handle_exception
async def _get_item_by_id(schema_name: str, table_name: str, item_id: int) -> list:
    async with async_session_maker() as session:
        query = text(
            f"SELECT * FROM {schema_name}.{table_name} WHERE id = :item_id"
        )
        result = await session.execute(query, {"item_id": item_id})
        rows = result.mappings().first()
        print(rows)
        if len(rows) != 0:
            return rows

        return ["Item not found"]


@handle_exception
async def _get_item_by_name(schema_name: str, table_name: str, item_name: str) -> list:
    async with async_session_maker() as session:

        query = text(
            f"SELECT * FROM {schema_name}.{table_name} WHERE name = {item_name}"
        )
        result = await session.execute(query)
        rows = result.fetchall()
        print(rows)
        if len(rows) != 0:
            return rows

        return None


@handle_exception
async def _get_item_by_telegram_id(
        schema_name: str,
        table_name: str,
        telegram_id: int
):
    async with async_session_maker() as session:
        query = text(
            f"SELECT * FROM {schema_name}.{table_name} WHERE telegram_id = {telegram_id}"
        )
        result = await session.execute(query)
        rows = result.fetchall()

        print(rows)
        if len(rows) != 0:
            return rows

        return "Item not found"


@handle_exception
async def _update_item_data(
        schema_name: str,
        table_name: str,
        item_id: int,
        item_data: any,
        item_column: str = None,
        query_param: str = "id"
) -> bool:
    async with async_session_maker() as session:
        if type(item_data) == dict:
            fields = ' ,'.join(
                [f"{key} = :{key}" for key in item_data.keys()])
            params = {**item_data, "item_id": int(item_id)}
        else:
            fields = f"{item_column} = :value"
            params = {"value": item_data, "item_id": int(item_id)}

        query = text(
            f"""UPDATE {schema_name}.{table_name}
                SET {fields}
                WHERE {query_param} = :item_id"""
        )
        result = await session.execute(query, params)
        await session.commit()

        if result.rowcount > 0:
            return {"func_status": "Item was updated✅"}
        else:
            return {"func_status": "Something went wrong❌"}


@handle_exception
async def _delete_item_by_id(
        schema_name: str,
        table_name: str,
        item_id: int,
) -> bool:
    async with async_session_maker() as session:
        query = text(
            f"DELETE FROM {schema_name}.{table_name} WHERE id = :item_id"
        )
        result = await session.execute(query, {"item_id": item_id})
        await session.commit()

        if result.rowcount > 0:
            return {"func_status": "Item was deleted✅"}
        else:
            return {"func_status": "Something went wrong❌"}


@handle_exception
async def _get_cook_work_schedule(telegram_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(WorkSchedule).where(
            WorkSchedule.telegram_id == telegram_id).order_by(WorkSchedule.work_date.desc()))
        cook_work_schedule = result.scalars().all()

        print(cook_work_schedule)
        if (cook_work_schedule):
            return cook_work_schedule
        else:
            return []


async def _update_user_data_by_telegram_id(
        user_table: Base,
        telegram_id: int,
        item_data: dict,
        additional_filters: dict | None = None
):
    async with async_session_maker() as session:
        try:
            conditions = [user_table.telegram_id == telegram_id]

            if additional_filters:
                for column, value in additional_filters.items():
                    conditions.append(column == value)

            result = await session.execute(
                select(user_table).where(*conditions)
            )

            user = result.scalars().first()

            if not user:
                return {"func_status": "User not found❗️"}

            for key, value in item_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            await session.commit()

            await session.refresh(user)

            return {"func_status": "Item was updated✅", "user": user}
        except Exception as e:
            return {"func_status": f"❌ Error {str(e)}"}


# orders = asyncio.run(_get_items_from_table_by_models(
#     Orders, ["delivery_date", "delivery_time"], "delivery_date", datetime.now().date()))
