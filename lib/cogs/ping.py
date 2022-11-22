from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord import Embed
from discord import Interaction
from discord import ui
from discord import ButtonStyle
from discord import utils
import discord

class Ping(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("Test cog ready...")
    
    @command(name="ping", aliases=["Ping"], 
        description='Sends a message: Pong!', 
        brief='Sends a message: Pong!')
    async def ping(self, ctx):
        await ctx.send("Pong!")

async def setup(bot: Bot):
    await bot.add_cog(Ping(bot))