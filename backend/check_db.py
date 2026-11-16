import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings


async def main():
    settings = get_settings()
    engine = create_async_engine(settings.database_url)

    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT version()"))
        print("Database connected successfully!")
        print(result.scalar())

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())