from lib.bot import bot
import asyncio

version = "0.1.0"

async def main():
    await bot.run(version)

asyncio.run(main())
