from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord.ext import commands
from discord import Embed
from discord import Interaction
from discord import ui
from discord import ButtonStyle
from discord import utils
from lib.cogs import gnpoll_ticket
from ..db import db

import discord

class ticket_launcher(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Create A Ticket", style=ButtonStyle.blurple, custom_id="create_ticket")
    async def create_ticket(self, interaction: Interaction, button: ui.Button):
        name = f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}"
        print(name)
        ticket = utils.get(interaction.guild.text_channels, name = f"ticket-for-{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.discriminator}")
        print(f"Channel: {ticket}")
        if ticket is not None:
            description = f"Link to your ticket: {ticket.mention}"
            embed = Embed(title="You have an open ticket.", description=description)
            await interaction.response.send_message()(embed=embed, ephemeral=True)
        else: 
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True), 
                # client.ticket_mod: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
            }
            try: 
                channel = await interaction.guild.create_text_channel(name=name, overwrites=overwrites)
                await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}!", ephemeral = True)
            except: return await interaction.response.send_message("Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral = True)
            embed = Embed(title="What would you like to do?")
            message = await channel.send(embed=embed, view = main())
        await interaction.message.delete()
    
    @ui.button(label="Cancel", style=ButtonStyle.red, custom_id="Cancel")
    async def close_interaction(self, interaction: Interaction, button: ui.Button):
        await interaction.message.delete()

class confirm(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        
    @ui.button(label = "Confirm", style = ButtonStyle.red, custom_id = "confirm")
    async def confirm_button(self, interaction, button):
        try: await interaction.channel.delete()
        except: await interaction.response.send_message("Channel deletion failed! Make sure I have `manage_channels` permissions!", ephemeral = True)

class main(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    
    @ui.button(label = "Gaming Night", style = ButtonStyle.blurple, custom_id = "gaming_night")
    async def test(self, interaction, button):
        embed = Embed(title = "Gaming Night Poll Options", description = "Gaming Night Games List", color=0x9900FF)
        games = db.records("SELECT GameID, GameName FROM games")
        value1 = ""
        value2 = ""
        for game in games:
            value1 += f"{game[0]} - {game[1]}" + "\n" # Old - value1 += f"{game[0]}" + "\n"
            #value2 += f"{game[1]}" + "\n"
            print(f"GameID: {game[0]}")
            print(f"GameName = {game[1]}")
        embed.add_field(name="GameID - GameName", value=value1)
        await interaction.channel.last_message.delete()
        await interaction.response.send_message(embed = embed, view = gnpoll_ticket.main())

    @ui.button(label = "Close Ticket", style = ButtonStyle.red, custom_id = "close_ticket")
    async def close(self, interaction, button):
        embed = Embed(title = "Are you sure you want to close this ticket?", color=0x9900FF)
        await interaction.response.send_message(embed = embed, view = confirm())

class TicketHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("Ticket_Handler cog ready...")

    @command(name="ticket", aliases=["Ticket"], 
        description='Creates a channel for the User, Admins, Mods, and the Bot and starts ticketing system.\nCurrently, you can only have one open ticket.', 
        brief='Creates a ticket.')
    @commands.has_any_role("Admin", "Mod")
    async def ticket(self, interaction: Interaction):
        await interaction.channel.last_message.delete()
        embed = Embed(title="Do you want to create a ticket?", description="Creating a ticket will redirect you to a private channel.", color=0x9900FF)
        await interaction.channel.send(embed=embed, view=ticket_launcher())

async def setup(bot: Bot):
    await bot.add_cog(TicketHandler(bot))