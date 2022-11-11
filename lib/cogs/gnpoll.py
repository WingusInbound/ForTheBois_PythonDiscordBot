from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord import Embed

from ..db import db

reactions = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:", ":regional_indicator_e:", ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:", ":regional_indicator_i:", ":regional_indicator_j:", ":regional_indicator_k:", ":regional_indicator_l:", ":regional_indicator_m:", ":regional_indicator_n:", ":regional_indicator_o:", ":regional_indicator_p:", ":regional_indicator_q:", ":regional_indicator_r:", ":regional_indicator_s:", ":regional_indicator_t:", ":regional_indicator_u:", ":regional_indicator_v:", ":regional_indicator_w:", ":regional_indicator_x:", ":regional_indicator_y:", ":regional_indicator_z:"]
emojis = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"]

class GNPoll(Cog):
    def __init__(self, bot):
        self.bot = bot
    @Cog.listener()
    async def on_ready(self):
        print("GNPoll cog listener...")

    @command(name="gn-add")
    async def gn_add(self, ctx):
        print("Received gn-add command")
        message = str(ctx.message.content)
        game_name = message.split(" ")
        print(game_name[1])
        db.execute(f"INSERT INTO games (GameName) Values ('{game_name[1]}')")
        db.commit()
    
    @command(name="gn-del")
    async def gn_del(self, ctx):
        print("Received gn-del command")
        message = str(ctx.message.content) # thoughts?????
        game = message.split(" ")
        game_id = game[1]
        record = db.record(f"Select * FROM games WHERE GameID={game_id}")
        print(record)
        command = f"DELETE FROM games WHERE GameID={game_id}"
        print(command)
        print(record[0])
        db.execute(command)
        db.commit()

    @command(name="gn-update")
    async def gn_update(self, ctx):
        print("Received gn-update command")
        message = str(ctx.message.content)
        game = message.split(" ")
        game_id = game[1]
        game_name = game[2]
        db.execute(f"UPDATE games SET GameName='{game_name}' WHERE GameID={game_id}")
        db.commit()

    @command(name="gn-list")
    async def gn_list(self, ctx):
        print("Received gn-list command")
        games = db.records("SELECT GameID, GameName FROM games")
        value1 = ""
        value2 = ""
        for game in games:
            value1 += f"{game[0]}" + "\n"
            value2 += f"{game[1]}" + "\n"
            print(f"GameID: {game[0]}")
            print(f"GameName = {game[1]}")
        embed = Embed(title="Gaming Night Games", color=0xFF0000)
        embed.add_field(name="GameID", value=value1)
        embed.add_field(name="GameName", value=value2, inline=True)
        message = await ctx.send(embed=embed)

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
        # await message.add_reaction("💖")

async def setup(bot: Bot):
    await bot.add_cog(GNPoll(bot))