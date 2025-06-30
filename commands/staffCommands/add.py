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

group = app_commands.Group(name = "staff", description = "The staff commands for Endure Core")

class Add(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
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
            staffModerator = staffGuild.get_role(int(staffMod))
            staffAdministrator = staffGuild.get_role(int(staffAdmin))
            staffRoleStaffCord = staffGuild.get_role(int(staffRole))
            mainModerator = mainGuild.get_role(int(mainMod))
            mainAdministrator = mainGuild.get_role(int(mainAdmin))
            mainStaffRole = mainGuild.get_role(int(mainStaff))
            clanStaffRole = clanGuild.get_role(int(clanStaff))
            directorStaffRole = directorGuild.get_role(int(directorStaff))
            toolModerator = toolGuild.get_role(int(toolGuildMod))
            toolAdministrator = toolGuild.get_role(int(toolGuildAdmin))
            toolGuildStaffRole = toolGuild.get_role(int(toolGuildStaff))
        except Exception as e:
            await errorChannel.send(f'```\n Roles Error\n\n{e}```')
            return
        try:
            roles = [
                staffModerator,
                staffAdministrator,
                staffRoleStaffCord,
                mainModerator,
                mainAdministrator,
                mainStaffRole,
                clanStaffRole,
                directorStaffRole,
                toolModerator,
                toolAdministrator,
                toolGuildStaffRole
            ]
            for staffRoles in roles:
                if staffRoles is None:
                    await errorChannel.send(staffRoles)
                    return
        except Exception as e:
            await errorChannel.send(f'``` \n Role Check Error \n\n{e}```')
            return
        for guild in guildArray:
            try:
                member = await guild.fetch_member(user.id)
            except discord.NotFound as e:
                await errorChannel.send(f'```\n Guild Error \n\n{e}```')
                await interaction.followup.send(f'User is not in `{guild.name}` - Exiting command')
                return
        # ^ Error check for guilds - then exit if they're not in a guild.
        logEmbed = discord.Embed(title = "Senior Staff Logs", description = "**New command usage**", color = 0xFF0FFF)
        logEmbed.add_field(name = "Command:", value = f'`/{interaction.command.name}`', inline = False)
        logEmbed.add_field(name = "New Staff:", value = user.mention, inline = False)
        logEmbed.add_field(name = "Command User:", value = interaction.user.mention, inline = False) 
        # define embed before giving roles
        try: # embed this
            for guild in guildArray:
                member = await guild.fetch_member(user.id)
                if role.value == "Moderator":
                    if guild == staffGuild:
                        await member.add_roles(staffModerator, staffRoleStaffCord)
                    elif guild == mainGuild:
                        await member.add_roles(mainModerator, mainStaffRole)
                    elif guild == clanGuild:
                        await member.add_roles(clanStaffRole)
                    elif guild == toolGuild:
                        await member.add_roles(toolModerator, toolGuildStaffRole)
                    elif guild == directorGuild:
                        await member.add_roles(directorStaffRole)
                if role.value == "Administrator":
                    if guild == staffGuild:
                        await member.add_roles(staffAdministrator, staffRoleStaffCord)
                    elif guild == mainGuild:
                        await member.add_roles(mainAdministrator, mainStaffRole)
                    elif guild == clanGuild:
                        await member.add_roles(clanStaffRole)
                    elif guild == toolGuild:
                        await member.add_roles(toolAdministrator, toolGuildStaffRole)
                    elif guild == directorGuild:
                        await member.add_roles(directorStaffRole)
            if role.value == "Moderator":
                logEmbed.add_field(name = "**Added Roles:**", value = f'`+`**Moderator/Staff Role** - **Staff Cord** \n `+`**Moderator/Staff Role** - **Main Guild** \n `+`**Staff Role** - **Clan Guild** \n `+`**Staff Role** - **Director Guild**', inline = False)
            if role.value == "Administrator":
                logEmbed.add_field(name = "**Added Roles:**", value = f'`+`**Admin/Staff Role** - **Staff Guild** \n `+`**Administrator/Staff Role** - **Main Guild** \n `+`**Staff Role** - **Clan Guild** \n `+`**Staff Role** - **Directors Guild**', inline = False)
        except Exception as e:
            await errorChannel.send(f'```\n Give Roles Error\n\n{e}```')
            return
        await interaction.followup.send(f'{user.mention} added to the Staff Team!', ephemeral = True)
        dmUser = await interaction.guild.fetch_member(config["dmUsers"][0])
        await dmUser.send(embed = logEmbed)
        try:
            await logsChannel.send(embed = logEmbed)
        except Exception as e:
            print(e)

async def setup(client: commands.Bot):
    await client.add_cog(Add(client), guild = discord.Object(id = int(config["seniorGuild"]["id"])))