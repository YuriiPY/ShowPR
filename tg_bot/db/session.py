from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import core.config

engine = create_async_engine(
    core.config.DATABASE_URL,
    future=True,
    echo=True
)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_db() -> AsyncGenerator:
    try:
        session: AsyncSession = async_session_maker()
        yield session
    finally:
        await session.close()


async def database_connection_test():
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
            print("✅TG_BOT: Database connection was successful")
    except Exception as e:
        print(f"❌TG_BOT: Connection to database was failed \nError: {e}")
