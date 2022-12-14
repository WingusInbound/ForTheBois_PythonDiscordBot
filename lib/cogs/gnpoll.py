from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord.ext import commands
from discord import Embed

from ..db import db

reactions = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:", ":regional_indicator_e:", ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:", ":regional_indicator_i:", ":regional_indicator_j:", ":regional_indicator_k:", ":regional_indicator_l:", ":regional_indicator_m:", ":regional_indicator_n:", ":regional_indicator_o:", ":regional_indicator_p:", ":regional_indicator_q:", ":regional_indicator_r:", ":regional_indicator_s:", ":regional_indicator_t:", ":regional_indicator_u:", ":regional_indicator_v:", ":regional_indicator_w:", ":regional_indicator_x:", ":regional_indicator_y:", ":regional_indicator_z:"]
emojis = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"]

class GNPoll(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("GNPoll cog ready...")
    '''
    @command(name="gnadd", 
        description='Adds a game to the Gaming Night Poll. \n Usage: [prefix]gnadd [Game Name to Add] \n Example: !gnadd Final Final Fantasy 420', 
        brief='Adds a game to the Gaming Night Poll.')
    @commands.has_any_role("Admin", "Mod")
    async def gn_add(self, ctx):
        print("Received gnadd command")
        message = str(ctx.message.content)
        game_name = message.split(" ", 1)
        print(game_name[1])
        db.execute(f"INSERT INTO games (GameName) Values ('{game_name[1]}')")
        db.commit()
    
    @command(name="gndel", 
        description='Deletes a game from the Gaming Night Poll. \n Usage: [prefix]gndel [Game id to Delete] *to get the game id run the command gnlist. \n Example: !gndel 2', 
        brief='Deletes a game from the Gaming Night Poll.')
    @commands.has_any_role("Admin", "Mod")
    async def gn_del(self, ctx):
        print("Received gndel command")
        message = str(ctx.message.content) # thoughts?????
        game = message.split(" ", 1)
        game_id = game[1]
        record = db.record(f"Select * FROM games WHERE GameID={game_id}")
        print(record)
        command = f"DELETE FROM games WHERE GameID={game_id}"
        print(command)
        print(record[0])
        db.execute(command)
        db.commit()

    @command(name="gnupdate", 
        description='Updates a game in the Gaming Night Poll. \n Usage: [prefix]gnupdate [Game id to Update] *to get the game id run the command gnlist. \n Example: !gnupdate 2 Final Fantasy 14',
        brief='Updates a game in the Gaming Night Poll.')
    @commands.has_any_role("Admin", "Mod")
    async def gn_update(self, ctx):
        print("Received gnupdate command")
        message = str(ctx.message.content)
        game = message.split(" ")
        game_id = game[1]
        game_name = game[2]
        db.execute(f"UPDATE games SET GameName='{game_name}' WHERE GameID={game_id}")
        db.commit()
    '''
    @command(name="gnlist", 
        description='Lists the games in the Gaming Night Poll. \n Usage: [prefix]gnlist. \n Example: !gnlist',
        brief='Lists the games in the Gaming Night Poll.')
    async def gn_list(self, ctx):
        print("Received gnlist command")
        games = db.records("SELECT GameID, GameName FROM games")
        value1 = ""
        value2 = ""
        for game in games:
            value1 += f"{game[0]} - {game[1]}" + "\n" # Old - value1 += f"{game[0]}" + "\n"
            #value2 += f"{game[1]}" + "\n"
            print(f"GameID: {game[0]}")
            print(f"GameName = {game[1]}")
        embed = Embed(title="Gaming Night Games", color=0xFF0000)
        embed.add_field(name="GameID - GameName", value=value1)
        message = await ctx.send(embed=embed)

    @command(name="gnpoll", 
        description='Generates the Gaming Night Poll. \n Usage: [prefix]gnpoll. \n Example: !gnpoll',
        brief='Generates the Gaming Night Poll.')
    async def gnpoll(self, ctx):
        games = db.records("SELECT GameName FROM games")
        
        value = ""
        i = 0
        for game in games:
            value += f"{reactions[i]} - " + game[0] + "\n"
            i += 1
        embed = Embed(title="Gaming Night Poll", description="Please react for the games you want to play", color=0x9900FF)
        embed.add_field(name="Games", value=value)
        message = await ctx.send(embed=embed)
        message = await message.fetch()
        for i in range(len(games)):
            await message.add_reaction(emojis[i])
            i += 1 
        # await message.add_reaction("💖")

async def setup(bot: Bot):
    await bot.add_cog(GNPoll(bot))