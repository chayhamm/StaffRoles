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
        await interaction.response.defer(ephemeral = True)
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
            guildArray = [staffGuild, mainGuild, clanGuild, directorGuild, toolGuild]
        except Exception as e:
            await interaction.followup.send("Error occured - not continuing with command.", ephemeral = True)
            await errorChannel.send(f'```\n Guilds Error\n\n{e}```')
            return
        try:
            # Get all roles in cords
            staffModerator = staffGuild.get_role(staffMod)
            staffAdministrator = staffGuild.get_role(staffAdmin)
            staffRoleStaffCord = staffGuild.get_role(staffRole)
            mainModerator = mainGuild.get_role(mainMod)
            mainAdministrator = mainGuild.get_role(mainAdmin)
            mainStaffRole = mainGuild.get_role(mainStaff)
            clanStaffRole = clanGuild.get_role(clanStaff)
            directorStaffRole = directorGuild.get_role(directorStaff)
            toolModerator = toolGuild.get_role(toolGuildMod)
            toolAdministrator = toolGuild.get_role(toolGuildAdmin)
            toolGuildStaffRole = toolGuild.get_role(toolGuildStaff)
        except Exception as e:
            await errorChannel.send(f'```\n Roles Error\n\n{e}```')
        for guild in guildArray:
            try:
                member = await guild.fetch_member(user.id)
            except discord.NotFound as e:
                await errorChannel.send(f'```\n Guild Error \n\n{e}')
                return
        # ^ Error check for guilds - then exit if they're not in a guild.
        try: # embed this
            if role == "Moderator":
                await member.add_roles(staffModerator)
                await member.add_roles(staffRoleStaffCord)
                await member.add_roles(mainModerator)
                await member.add_roles(mainStaffRole)
                await member.add_roles(clanStaffRole)
                await member.add_roles(toolModerator)
                await member.add_roles(toolGuildStaffRole)
        except Exception as e:
            await errorChannel.send(f'```\n Give Roles Error\n\n{e}```')
        logEmbed = discord.Embed(title = "Senior Staff Logs", description = "new command usage", color = 0xFF0FFF)
        logEmbed.add_field(name = "command:", value = f'`/{interaction.command.name}`', inline = False)
        logEmbed.add_field(name = "new staff:", value = user.mention, inline = False)
        logEmbed.add_field(name = "user:", value = interaction.user.mention, inline = False)
        await interaction.followup.send(f'{user.mention} added to the Staff Team!', ephemeral = True)
        dmUser = await interaction.guild.fetch_member(config["dmUsers"][0])
        await dmUser.send(embed = logEmbed)
        try:
            await logsChannel.send(embed = logEmbed)
        except Exception as e:
            print(e)

async def setup(client: commands.Bot):
    await client.add_cog(Add(client))