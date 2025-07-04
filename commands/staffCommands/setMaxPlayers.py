import discord
from discord.app_commands import Group, command
from discord.ext.commands import GroupCog
from discord.ext import commands
import json
from datetime import datetime
import aiohttp

with open("config.json") as config:
    config = json.load(config)

class SetMax(GroupCog, group_name = "set", group_description = "Group for the maxplayers command."):
    @command(name = "maxplayers", description = "Command to set the max players of the Server.")
    async def max(self, interaction: discord.Interaction, count: int):
        await interaction.response.defer(ephemeral = True)
        guild = interaction.guild
        chay = await guild.fetch_member(int(config["chayID"]))
        logsChannel = await guild.fetch_channel(config["seniorGuild"]["2xLogs"])
        apiKey = config["API"]
        uuid = config["UUID"]
        command = f'server.maxplayers {count}'
        url = f'http://51.77.68.69/api/client/servers/{uuid}/command'
        headers = {
            "Authorization": f'Bearer {apiKey}',
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "command": command
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers = headers,  json = payload) as response:
                if response.status == 204:
                    await interaction.followup.send(f"✅ Command sent! Player count now set to `{count}`")
                    embed = discord.Embed(title = "Endure | 2X Alerts", description = "The max player count has been updated!", color = 0xFF0000)
                    embed.add_field(name = "**Player count:**", value = f'`{count}`', inline = False)
                    embed.add_field(name = "**User:**", value = interaction.user.mention, inline = False)
                    embed.set_footer(text = datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                    await guild.owner.send(embed = embed)
                    await chay.send(embed = embed)
                    try:
                        await logsChannel.send(embed = embed)
                    except Exception as e:
                        print(e)
                else:
                    await interaction.followup.send(f"Command not sent! Status code: {response.status}")
                    await guild.owner.send(f'{interaction.user.mention} tried to use the `/set {interaction.command.name}` command - but failed.')
                    await chay.send(f'{interaction.user.mention} tried to use the `/set {interaction.command.name}` command - but failed.')

async def setup(client: commands.Bot):
    await client.add_cog(SetMax(), guild = discord.Object(id=int(config["seniorGuild"]["id"])))