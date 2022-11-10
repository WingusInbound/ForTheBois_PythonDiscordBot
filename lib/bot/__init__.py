from glob import glob
from asyncio import sleep
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord.ext.commands import when_mentioned_or
from discord import Intents
from discord import Embed
from datetime import datetime
from ..db import db

owner_ids = [211318514613616640]
prefix = "!"
cogs = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
print(cogs)
intents = Intents.default()
intents.message_content = True
intents.members = True

def get_prefix(bot, message):
    db.field("SELECT Prefix FROM Guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in cogs:
            setattr(self, cog, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"Cog Loaded: {cog}")
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in cogs])

class Bot(BotBase):
    def __init__(self):
        # self.prefix = prefix
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix, owner_ids=owner_ids, intents=intents)
    
    async def setup(self):
        for filename in os.listdir("./lib/cogs"):
            if filename.endswith(".py"):
            # cut off the .py from the file name
                await bot.load_extension(f"lib.cogs.{filename[:-3]}")
        
        print("Setup complete.")
    
    async def run(self, version):
        self.version = version

        print("running setup...")
        await self.setup()

        with open("./lib/bot/token.env", "r", encoding="utf-8") as token_file:
            self.token = token_file.read()

        print("running bot...")
        await super().start(self.token, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
        channel = self.get_channel(923369111336140850)
        await channel.send("An error occured.")
        raise
    
    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            pass

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(835975742663032852)
            self.stdout = self.get_channel(923369111336140850)
            self.scheduler.start()
            
            # print("bot ready")
            await self.stdout.send("Now Online!")
            print(" bot ready...")

            embed = Embed(title="Now Online!", description="For The Bois is now online.", color=0xFF0000, timestamp=datetime.utcnow())
            fields = [("Name", "Value", True),
                ("Another field", "This field is next to the other one.", True),
                ("A non-inline field", "This field will appear on it's own row.", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="For The Bois", icon_url=self.guild.icon.url)
            embed.set_footer(text="This is a footer!")
            embed.set_thumbnail(url=self.guild.icon.url)
            embed.set_image(url=self.guild.icon.url)
            await self.stdout.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            # print(message)
            await self.process_commands(message)

bot = Bot()
