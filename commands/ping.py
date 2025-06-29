import discord
from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name = "ping", description = "Command to check if the bot is still online.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong!", ephemeral = True)

async def setup(client: commands.Bot):
    await client.add_cog(Ping(client))