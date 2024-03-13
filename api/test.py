from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text
import asyncio
import os

DB_USER = os.getenv("DB_USER", "test")
DB_PASSWORD = os.getenv("DB_PASSWORD", 'test')
DB_NAME = os.getenv("DB_NAME", 'postgres')
DB_HOST = os.getenv("DB_HOST", 'localhost')
DB_PORT = os.getenv("DB_PORT", 5432)

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 
print(DATABASE_URL)

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session


async def main():
    async with async_session() as session:
        try:
            # Example: Fetch some data
            query = """
SELECT * FROM betmodel"""
            results = await session.execute(text(query))
            for row in results.all():
                print(row)

            await session.commit()

        except Exception as e: 
            await session.rollback() 
            print(f"Error during database interaction: {e}")


if __name__ == "__main__":
    asyncio.run(main())