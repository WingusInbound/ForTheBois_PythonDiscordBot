from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
import discord
import random
from discord import Embed

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("Fun cog ready...")
    
    @command(name="fireball", aliases=["Fireball"], 
        description="Cast the spell Fireball. \n A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one. The fire spreads around corners. It ignites flammable objects in the area that aren't being worn or carried.", 
        brief='Cast the spell Fireball.')
    async def fireball(self, ctx):
        message = str(ctx.message.content)
        message_array = message.split(" ")
        if len(message_array) > 1:
            print("Setting Target to Provided @mention")
            target = message_array[1]
        else:
            print("Rolled a Nat 1")
            target = ctx.message.author.mention
        total = 0
        for _ in range(8):
            roll = random.randint(1, 6)
            print(roll)
            total += roll
        print(total)
        embed = Embed(title=f"{ctx.message.author.display_name} casts Fireball!",
            description="Saving Throw: Dexterity \n Success: Half Damage \n Roll: 8d6 (at level 3 - 1d6 for each level above 3) ", 
            color=0xFF0000)
        target = str(target)
        embed.add_field(name="Target", value=target, inline=False)
        total = str(total) + " Fire"
        embed.add_field(name="Damage", value=total, inline=False)
        await ctx.send(embed=embed)
    
async def setup(bot: Bot):
    await bot.add_cog(Fun(bot))