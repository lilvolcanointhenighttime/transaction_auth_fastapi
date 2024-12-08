from ..models import Base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .env import DB_URL


engine = create_async_engine(
    DB_URL
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
