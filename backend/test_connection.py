import asyncio

import asyncpg


async def main():
    try:
        conn = await asyncpg.connect(
            host="127.0.0.1",
            port=5434,
            user="researchos",
            password="researchos",
            database="researchos",
        )
        print("RAW CONNECTION SUCCESS")
        print(await conn.fetchval("SELECT current_database()"))
        await conn.close()
    except Exception as e:
        print("RAW CONNECTION FAILED:", repr(e))

asyncio.run(main())
