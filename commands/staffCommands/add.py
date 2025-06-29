import discord
from discord import app_commands
from discord.ext import commands
import json

with open("config.json") as config:
    config = json.load(config)

class Add(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    group = app_commands.Group(name = "staff", description = "The staff commands for Endure Core")
    @group.command(name = "add", description = "Add a new staff member")
    async def add(self, interaction: discord.Interaction, user: discord.User):
        guild = self.client.get_guild(int(config["seniorGuild"]["id"]))
        logsChannel = await guild.fetch_channel(config["seniorGuild"]["logs"])
        logEmbed = discord.Embed(title = "Senior Staff Logs", description = "new command usage", color = 0xFF0FFF)
        logEmbed.add_field(name = "command:", value = f'`/{interaction.command.name}`', inline = False)
        logEmbed.add_field(name = "new staff:", value = user.mention, inline = False)
        logEmbed.add_field(name = "user:", value = interaction.user.mention, inline = False)
        await interaction.response.send_message(f'{user.mention} added to the Staff Team!', ephemeral = True)
        try:
            await logsChannel.send(embed = logEmbed)
        except Exception as e:
            print(e)

async def setup(client: commands.Bot):
    await client.add_cog(Add(client))