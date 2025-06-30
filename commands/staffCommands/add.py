import discord
from discord import app_commands
from discord.ext import commands
import json

with open("config.json") as config:
    config = json.load(config)

staffGuildID = config["staffGuild"]["id"]
staffRoles = config["staffGuild"]["roles"]
staffMod = staffRoles["mod"]
staffAdmin = staffRoles["admin"]
staffRole = staffRoles["staff"]

mainGuildID = config["mainGuild"]["id"]
mainRoles = config["mainGuild"]["roles"]
mainMod = mainRoles["mod"]
mainAdmin = mainRoles["admin"]
mainStaff = mainRoles["staff"]

clanGuildID = config["clanGuild"]["id"]
clanRoles = config["clanGuild"]["roles"]
clanStaff = clanRoles["staff"]

directorGuildID = config["directorGuild"]["id"]
directorRoles = config["directorGuild"]["roles"]
directorStaff = directorRoles["staff"]

toolGuildID = config["toolsGuild"]["id"]
toolGuildRoles = config["toolsGuild"]["roles"]
toolGuildMod = toolGuildRoles["mod"]
toolGuildAdmin = toolGuildRoles["admin"]
toolGuildStaff = toolGuildRoles["staff"]

class Add(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    group = app_commands.Group(name = "staff", description = "The staff commands for Endure Core")
    @group.command(name = "add", description = "Add a new staff member")
    @app_commands.choices(role=[
        app_commands.Choice(name = "Moderator", value = "Moderator"),
        app_commands.Choice(name = "Administrator", value = "Administrator")
    ])
    async def add(self, interaction: discord.Interaction, user: discord.User, role: app_commands.Choice[str]):
        guild = self.client.get_guild(int(config["seniorGuild"]["id"]))
        logsChannel = await guild.fetch_channel(config["seniorGuild"]["logs"])
        errorChannel = await guild.fetch_channel(config["seniorGuild"]["error"])
        try:
            # Get all guilds
            staffGuild = await self.client.fetch_guild(int(staffGuildID))
            mainGuild = await self.client.fetch_guild(int(mainGuildID))
            clanGuild = await self.client.fetch_guild(int(clanGuildID))
            directorGuild = await self.client.fetch_guild(int(directorGuildID))
            toolGuild = await self.client.fetch_guild(int(toolGuildID))
        except Exception as e:
            await interaction.response.send_message("Error occured - not continuing with command.", ephemeral = True)
            await errorChannel.send(f'```\n Guilds Error\n\n{e}```')
            return
        try:
            # Get all roles in cords
            staffModerator = await staffGuild.get_role(staffMod)
            staffAdministrator = await staffGuild.get_role(staffAdmin)
            staffRoleStaffCord = await staffGuild.get_role(staffRole)
            mainModerator = await mainGuild.get_role(mainMod)
            mainAdministrator = await mainGuild.get_role(mainAdmin)
            mainStaffRole = await staffGuild.get_role(mainStaff)
            clanStaffRole = await clanGuild.get_role(clanStaff)
            directorStaffRole = await directorGuild.get_role(directorStaff)
            toolModerator = await toolGuild.get_role(toolGuildMod)
            toolAdministrator = await toolGuild.get_role(toolGuildAdmin)
            toolGuildStaffRole = await toolGuild.get_role(toolGuildStaff)
        except Exception as e:
            await errorChannel.send(f'```\n Roles Error\n\n{e}```')
        if user not in staffGuild:
            await interaction.response.send_message("User not in Staff Guild!", ephemeral = True)
            return
        if user not in mainGuild:
            await interaction.response.send_message("User not in Main Guild!", ephemeral = True)
            return
        if user not in clanGuild:
            await interaction.response.send_message("User not in Clan Guild!", ephemeral = True)
            return
        if user not in directorGuild:
            await interaction.response.send_message("User not in Director Guild!", ephemeral = True)
            return
        if user not in toolGuild:
            await interaction.response.send_message("User not in Tools Guild!", ephemeral = True)
            return
        # ^ Error check for guilds - then exit if they're not in a guild.
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