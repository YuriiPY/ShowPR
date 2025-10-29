import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from functools import partial
from sqlalchemy import text
from sqlalchemy import NullPool

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.core.config import TEST_DATABASE_URL
from app.db.models.Menu.products_models import Dumplings

create_async_engine = partial(create_async_engine, poolclass=NullPool)

engine = create_async_engine(
    TEST_DATABASE_URL,
    future=True
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def db_engine_fixture():
    async with engine.begin() as connection:
        await connection.execute(text("CREATE SCHEMA IF NOT EXISTS menu;"))
        await connection.execute(text("CREATE SCHEMA IF NOT EXISTS order_data;"))
        await connection.execute(text("CREATE SCHEMA IF NOT EXISTS menu_table_names;"))

        await connection.execute(text("""
        DO $$ BEGIN 
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'product_type') THEN 
                CREATE TYPE menu.product_type as ENUM ('by weight', 'by portion');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status') THEN 
                CREATE TYPE order_data.order_status as ENUM ('pending','processing','shipped','delivered','canceled','returned','ready to delivery');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'delivery_type') THEN 
                CREATE TYPE order_data.delivery_type as ENUM ('delivery','contactless delivery','own collection');
            END IF;
        END $$;
        """))

        await connection.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def session(db_engine_fixture: AsyncEngine):
    async_session = async_sessionmaker(
        db_engine_fixture, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope='function', autouse=True)
async def seed_data(session: AsyncSession):

    items = [
        Dumplings(
            name=f"Dumpling #{i}",
            name_ua=f"Вареник #{i}",
            name_pl=f"Pieróg #{i}",
            description=f"Delicious dumpling #{i}",
            description_ua=f"Смачний вареник #{i}",
            description_pl=f"Pyszny pieróg #{i}",
            price=100 + i,
            type="by portion",
            img="https://i.ibb.co/pB7k5PHx/dumplings2.jpg",
            status=True,
        ) for i in range(1, 4)
    ]

    session.add_all(items)
    await session.commit()
    yield session


@pytest_asyncio.fixture(scope='function')
async def client(session: AsyncSession):

    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
