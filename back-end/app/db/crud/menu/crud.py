from functools import wraps
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import LargeBinary, MetaData, text
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from app.db.session import get_db
from app.db.models.Menu.products_models import *
from app.db.enums import ProductsTypes
from app.schemas.products import ItemsCreate

# id = Column(Integer, primary_key=True, autoincrement=True)
# name = Column(String, nullable=True)
# description = Column(String(255), nullable=True)
# price = Column(Integer, nullable=True)
# type = Column(Enum(ProductsTypes), nullable=True)
# img = Column(LargeBinary, nullable=True)
# status = Column(bool, nullable=True, default=False)


# async def create_item(
#     name: str,
#     description: str,
#     price: int,
#     type: ProductsTypes,
#     img: bytes,
#     status: bool,
#     db: AsyncSession
# ) -> Dumplings:
#     new_item = Dumplings(
#         name=name,
#         description=description,
#         price=price,
#         type=type,
#         img=img,
#         status=status
#     )
#     db.add(new_item)
#     await db.commit()
#     await db.refresh(new_item)
#     return new_item

def handle_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f'❌ Error in {func.__name__}: {e}')
            raise e

    return wrapper


@handle_exception
async def create_menu_product(
    table: DeclarativeMeta,
    db: AsyncSession,
    item: ItemsCreate
):
    new_item = table(
        name=item.name,
        name_ua=item.name_ua,
        name_pl=item.name_pl,
        price=item.price,
        type=item.type.value,
        status=item.status,
        img=item.img,
        description=item.description,
        description_ua=item.description_ua,
        description_pl=item.description_pl
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@handle_exception
async def create_new_item(
    table: DeclarativeMeta,
    db: AsyncSession,
    field: dict,
):
    new_item = table(**field)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@handle_exception
async def get_all_items(
        table: DeclarativeMeta,
        db: AsyncSession
):
    result = await db.execute(select(table))
    return result.scalars().all()


@handle_exception
async def get_item_by_id(
    table: DeclarativeMeta,
    item_id: int,
    db: AsyncSession
):
    result = await db.execute(select(table).where(table.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise NoResultFound(
            f'Item with ID{item_id} not found in table {table.__tablename__}')
    return item


@handle_exception
async def update_item(
    table: DeclarativeMeta,
    item_id: int,
    db: AsyncSession,
    **fields
):
    item = await get_item_by_id(table, item_id, db)

    for key, value in fields.items():
        if hasattr(item, key):
            setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return item


@handle_exception
async def delete_item(
    table: DeclarativeMeta,
    item_id: int,
    db: AsyncSession
):
    item = await get_item_by_id(table, item_id, db)
    await db.delete(item)
    await db.commit()


@handle_exception
async def get_table_name(
    db: AsyncSession
):

    query = text(f"""SELECT tablename
                 FROM pg_catalog.pg_tables
                 WHERE schemaname = :schemaname""")
    result = await db.execute(query, {"schemaname": "menu"})
    print(result)
    tables = [row["tablename"] for row in result.mappings().all()]
    print(tables)
    return tables


@handle_exception
async def _get_table_models_in_schema(
    db: AsyncSession,
    schema: str
) -> tuple:

    engine = db.bind
    metadata = MetaData(schema=schema)

    async with engine.begin() as connection:
        await connection.run_sync(metadata.reflect, schema=schema)

    tables = metadata.tables

    return tables


@handle_exception
async def _get_tables_in_schema(
    db: AsyncSession,
    schema: str
) -> tuple:

    query = text(
        f"SELECT * FROM pg_catalog.pg_tables WHERE schemaname='{schema}'")
    result = await db.execute(query, {"schema": schema})

    tables = [row[1] for row in result.fetchall()]

    return tables


@handle_exception
async def get_all_data_from_tables(
        db: AsyncSession
):
    tables_names = await get_table_name(db)

    tables = {
        'dumplings': Dumplings,
        'soups': Soups,
        'meats': Meats,
        'cakes': Cakes,
        'frozen_dumplings': Frozen_Dumplings,
        'frozen_meats': Frozen_Meats
    }

    all_data = {
        "cookedMenu": {},
        "frozenMenu": {}
    }
    for table_name in tables_names:
        # FIXME:
        # class table(ProductModel):
        #     __tablename__ = table

        table = tables.get(table_name, "")
        result = await get_all_items(table, db)

        table_data = {
            row.id: {
                key: value for key, value in row.__dict__.items()
            } for row in result
        }

        if "frozen_" not in table_name:
            all_data["cookedMenu"].update({table_name: table_data})
        elif "frozen_" in table_name:
            all_data["frozenMenu"].update({table_name: table_data})

    return all_data
