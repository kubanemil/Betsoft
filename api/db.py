import os
import typing

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    os.environ["DB_USER"],
    os.environ["DB_PASSWORD"],
    os.environ["DB_HOST"],
    os.environ["DB_PORT"],
    os.environ["DB_NAME"],
)

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with async_session() as session:
        yield session


session_dep = typing.Annotated[AsyncSession, Depends(get_session)]
