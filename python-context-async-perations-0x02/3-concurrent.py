import aiosqlite
import asyncio


async def async_fetch_users():
    async with aiosqlite.connect("alx_database") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            result = [row async for row in cursor]
            return result


async def async_fetch_older_users():
    async with aiosqlite.connect("alx_database") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            result = [row async for row in cursor]
            return result


async def fetch_concurrently():
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())


asyncio.run(fetch_concurrently())
