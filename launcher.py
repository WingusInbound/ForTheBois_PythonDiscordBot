from lib.bot import bot
import asyncio

version = "0.0.1"

async def main():
    await bot.run(version)

asyncio.run(main())
