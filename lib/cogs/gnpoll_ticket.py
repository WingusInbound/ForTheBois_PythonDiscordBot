from discord.ext.commands import Bot, Cog
from discord.ext.commands import command
from discord import Embed
from discord import Interaction
from discord import ui
from discord import ButtonStyle
from discord import utils
from ..db import db
from lib.cogs import ticket_handler

import discord

class main(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    
    @ui.button(label = "Add Game", style = ButtonStyle.blurple, custom_id = "add_game")
    async def add_game(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(add_game())

    @ui.button(label = "Delete Game", style = ButtonStyle.success, custom_id = "delete_game")
    async def delete_game(self, interaction, button):
        await interaction.response.send_modal(delete_by_game_id())
        
    @ui.button(label = "Update Game", style = ButtonStyle.success, custom_id = "update_game")
    async def upgate_game(self, interaction, button):
        await interaction.response.send_modal(update_game())
    
    @ui.button(label = "Close Ticket", style = ButtonStyle.red, custom_id = "close_ticket")
    async def close(self, interaction, button):
        embed = Embed(title = "Are you sure you want to close this ticket?", color=0x9900FF)
        await interaction.response.send_message(embed = embed, view = confirm_close_ticket())

class confirm_close_ticket(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        
    @ui.button(label = "Confirm", style = ButtonStyle.red, custom_id = "confirm")
    async def confirm_button(self, interaction, button):
        try: await interaction.channel.delete()
        except: await interaction.response.send_message("Channel deletion failed! Make sure I have `manage_channels` permissions!", ephemeral = True)

class confirm_cancel_command(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @ui.button(label = "Confirm", style = ButtonStyle.red, custom_id = "confirm")
    async def confirm_button(self, interaction, button):
        try: 
            embed = Embed(title="What would you like to do?")
            await interaction.response.send_message(embed=embed, view = ticket_handler.main())
            await interaction.message.delete()
            await interaction.message.delete()                                                      
        except: 
            embed = Embed(title="General Error", 
            description="Sorry....My bad!\n ~ Wingus")
            await interaction.response.send_message("General Error....Sorry My Bad. ~Wingus ")

class add_game(ui.Modal, title="Add A Game"):
    def __init__(self) -> None:
        super().__init__()

    game_name = ui.TextInput(label= "Game Name: ")

    async def on_submit(self, interaction):
        print(self.game_name.label)
        print(self.game_name)
        command = f"INSERT INTO games (GameName) Values ('{self.game_name}')"
        print(command)
        db.execute(command)
        db.commit()
        embed = Embed(title = "Gaming Night Poll Options", description = f"Added Game: {self.game_name}", color=0x9900FF)
        games = db.records("SELECT GameID, GameName FROM games")
        value1 = ""
        value2 = ""
        for game in games:
            value1 += f"{game[0]} - {game[1]}" + "\n" # Old - value1 += f"{game[0]}" + "\n"
            #value2 += f"{game[1]}" + "\n"
            print(f"GameID: {game[0]}")
            print(f"GameName = {game[1]}")
        embed.add_field(name="GameID - GameName", value=value1)
        await interaction.response.send_message(embed=embed, view=main())
        await interaction.message.delete()

class delete_by_game_id(ui.Modal, title="Delete A Game"):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    
    game_id = ui.TextInput(label="GameID: ")

    async def on_submit(self, interaction):
        print(self.game_id.label)
        print(self.game_id)
        record = db.record(f"Select * FROM games WHERE GameID={self.game_id}")
        print(record)
        if record is None:
            await interaction.response.send_message(f"No Record with ID: {self.game_id}")
        else:
            command = f"DELETE FROM games WHERE GameID={record[0]}"
            print(command)
            db.execute(command)
            db.commit()
            description=f"Deleted Game: {record[0]} - {record[1]}"
            embed = Embed(title = "Gaming Night Poll Options", description = description, color=0x9900FF)
            games = db.records("SELECT GameID, GameName FROM games")
            value1 = ""
            value2 = ""
            for game in games:
                value1 += f"{game[0]} - {game[1]}" + "\n" # Old - value1 += f"{game[0]}" + "\n"
                #value2 += f"{game[1]}" + "\n"
                print(f"GameID: {game[0]}")
                print(f"GameName = {game[1]}")
            embed.add_field(name="GameID - GameName", value=value1)
            await interaction.response.send_message(embed=embed, view=main())
            await interaction.message.delete()

class update_game(ui.Modal, title="Update A Game"):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    game_id = ui.TextInput(label="GameID: ")
    game_name = ui.TextInput(label="Game Name: ")
    
    async def on_submit(self, interaction):
        print(f"GameID: {self.game_id} | GameName: {self.game_name}")
        record = db.record(f"Select * FROM games WHERE GameID={self.game_id}")
        print(record)
        if record is None:
            await interaction.response.send_message(f"No Record with ID: {self.game_id}")
        else:
            command = f"UPDATE games SET GameName='{self.game_name}' WHERE GameID={self.game_id}"
            print(command)
            db.execute(command)
            db.commit()
            description=f"Old Game Record: {record[0]} - {record[1]}\nNew Game Record: {self.game_id} - {self.game_name}"
            embed = Embed(title = "Gaming Night Poll Options", description = description, color=0x9900FF)
            games = db.records("SELECT GameID, GameName FROM games")
            value1 = ""
            value2 = ""
            for game in games:
                value1 += f"{game[0]} - {game[1]}" + "\n" # Old - value1 += f"{game[0]}" + "\n"
                #value2 += f"{game[1]}" + "\n"
                print(f"GameID: {game[0]}")
                print(f"GameName = {game[1]}")
            embed.add_field(name="GameID - GameName", value=value1)
            await interaction.response.send_message(embed=embed, view=main())
            await interaction.message.delete()

class GNPoll_Ticket(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("TestUI cog ready...")

async def setup(bot: Bot):
    await bot.add_cog(GNPoll_Ticket(bot))
