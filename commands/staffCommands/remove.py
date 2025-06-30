import discord
from discord import app_commands
from discord.ext import commands
import json

with open("config.json") as config:
    config = json.load(config)

class Remove(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    group = app_commands.Group(name = "staff", description = "Staff commands")
    @group.command(name = "remove", description = "Remove a staff member")
    async def remove(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer(ephemeral = True)
        await interaction.followup.send("Testing", ephemeral = True)

async def setup(client: commands.Bot):
    await client.add_cog(Remove(client), guild = discord.Object(id = int(config["seniorGuild"]["id"])))