# For The Bois Discord Bot
# Author Joe Arangio

import asyncio
import discord
from discord.ext import commands 
import json
import os

# Debug Switch
debug = True

# Open config.json file
config_file = open('config.json')

# load JSON as dictionary
config = json.load(config_file)

# Close config.json file
config_file.close

# Sets token variable
token = config["Token"]

# Sets prefix
prefix = config["Prefix"]

# Setting Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix=prefix,intents=intents)

# on_ready event
@client.event
async def on_ready():
    print(f'{client.user} is online.')

# on_message_edit event
@client.event
async def on_message_edit(before, after):
    await before.channel.send(
        f'{before.author} edited a message.\n'
        f'Before: {before.content}\n'
        f'After: {after.content}'
    )

@client.command()
async def info(ctx: discord.Interaction):
    embed = discord.Embed(title=f'Information about {client.user} ')
    embed.add_field(name='Description', value='A Discord bot for The Bois.', inline=False)
    await ctx.send(embed=embed)

@client.group(name='helpcmd', invoke_without_command=True)
async def helpcmd(ctx):
    await ctx.send('Base Help Command. Subcommands: Poll, Ping')

@helpcmd.command(name='Poll')
async def poll_subcommand(ctx):
    await ctx.send('Poll Help Text')

@helpcmd.command(name='Ping')
async def poll_subcommand(ctx):
    await ctx.send('Ping Help Text')

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with client:
        await load_extensions()
        await client.start(token)

asyncio.run(main())