from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord.ext import commands
from discord import Embed

import os

class Owner(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("Owner cog ready...")
    
    @command(name="reload", 
        description='Reloads the cog specified', 
        brief='Reloads the cog specified')
    @commands.is_owner()
    async def reload(self, ctx, *, name: str):
        try:
            await self.bot.reload_extension(f"lib.cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog reloaded')

    @command(name="reload-all", aliases=["RA","ra"],
        description='Reloads all cogs', 
        brief='Reloads all cogs')
    @commands.is_owner()
    async def reloadall(self, ctx):
        for filename in os.listdir("./lib/cogs"):
            if filename.endswith(".py"):
                cog_name = f"{filename[:-3]}"           
                try:
                    await self.bot.reload_extension(f"lib.cogs.{cog_name}")
                    self.bot.cogs_ready.ready_up(f"{cog_name}")
                except Exception as e:
                    return await ctx.send(e)
        await ctx.send(f'All Cogs Reloaded!')

    @command(name="load", 
        description='Loads the cog specified', 
        brief='Loads the cog specified')
    @commands.is_owner()
    async def load(self, ctx, *, name: str):
        try:
            await self.bot.load_extension(f"lib.cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog loaded')

    @command(name="unload", 
        description='Unloads the cog specified', 
        brief='Unloads the cog specified')
    @commands.is_owner()
    async def unload(self, ctx, *, name: str):
        try:
            await self.bot.unload_extension(f"lib.cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog unloaded')


async def setup(bot: Bot):
    await bot.add_cog(Owner(bot))