import discord
from discord.app_commands import Group, command
from discord.ext.commands import GroupCog
from discord.ext import commands
import json
from datetime import datetime
from aiorcon import RCON

with open("config.json") as config:
    config = json.load(config)

class Team(GroupCog, group_name = "team", group_description = "Team info commands"):
    @command(name = "info", description = "Command to check a team's info ingame - uses CLANS REBORN.")
    async def info(self, interaction: discord.Interaction, clannameorsteam: str):
        await interaction.response.defer(ephemeral = True)
        guild = interaction.guild
        command_text = f'clans show {clannameorsteam}'
        try:
            async with RCON(config["rcon"]["rconIP"], port = int(config["rcon"]["rconPort"]), password = config["rcon"]["rconPassword"]) as rcon:
                output = await rcon.command(command_text)
                embed = discord.Embed(title = "Endure 2x | EU | Team information", description = f'Information for: `{clannameorsteam}`', color = 0xFFA500)
                embed.add_field(name = "**Team:**", value = f'```{output}```', inline = False)
                embed.add_field(name = "**User:**", value = interaction.user.mention, inline = False)
                embed.set_footer(text = datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

async def setup(client: commands.Bot):
    await client.add_cog(Team(), guild = discord.Object(id = int(config["staffGuild"]["id"])))