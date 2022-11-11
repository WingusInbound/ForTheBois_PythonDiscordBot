from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord import Embed

class Test(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("Test cog listener...")
    
    @command(name="ping", aliases=["Ping"])
    async def ping(self, ctx):
        await ctx.send("Pong!")

async def setup(bot: Bot):
    await bot.add_cog(Test(bot))