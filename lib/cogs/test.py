from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord import Embed

from ..db import db

reactions = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:", ":regional_indicator_e:", ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:", ":regional_indicator_i:", ":regional_indicator_j:", ":regional_indicator_k:", ":regional_indicator_l:", ":regional_indicator_m:", ":regional_indicator_n:", ":regional_indicator_o:", ":regional_indicator_p:", ":regional_indicator_q:", ":regional_indicator_r:", ":regional_indicator_s:", ":regional_indicator_t:", ":regional_indicator_u:", ":regional_indicator_v:", ":regional_indicator_w:", ":regional_indicator_x:", ":regional_indicator_y:", ":regional_indicator_z:"]
emojis = ["🇦", "🇧", "🇨", "🇩", "🇪"]

class Test(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Test cog listener...")

    @command(name="ping", aliases=["Ping"])
    async def ping(self, ctx):
        await ctx.send("Pong!")
    
    @command(name="gnpoll")
    async def gnpoll(self, ctx):
        games = db.records("SELECT GameName FROM games")
        # print(games)
        value = ""
        i = 0
        count = 0
        for game in games:
            value += f"{reactions[i]} - " + game[0] + "\n"
            count += 1
            i += 1
        embed = Embed(title="Gaming Night Poll", description="Please react for the games you want to play", color=0xFF0000)
        embed.add_field(name="Games", value=value)
        message = await ctx.send(embed=embed)
        message = await message.fetch()
        for i in range(len(games)):
            await message.add_reaction(emojis[i])
            i += 1 
        await message.add_reaction("💖")

async def setup(bot: Bot):
    await bot.add_cog(Test(bot)) 
    
    
        

    