import discord
from discord.ext import commands
from discord import app_commands
import json
import os

with open("config.json") as config:
    config = json.load(config)

intents = discord.Intents.all()
client = commands.Bot(command_prefix = config["prefix"], intents = intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    try:
        client.tree.clear_commands(guild = discord.Object(id = int(config["seniorGuild"]["id"])))
        synced = await client.tree.sync(guild = discord.Object(id=int(config["seniorGuild"]["id"])))
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

async def main():
    try:
        for file in os.listdir("commands"):
            if file.endswith(".py"):
                ext = file[:-3]
                path = f'commands.{ext}'
                await client.load_extension(path)
                print(f'Loaded: {path}')
        for sFile in os.listdir("commands/staffCommands"):
            if sFile.endswith(".py") and sFile != "group.py":
                extension = sFile[:-3]
                pathOne = f'commands.staffCommands.{extension}'
                await client.load_extension(pathOne)
                print(f'Loaded: {pathOne}')
    except Exception as e:
        print(e)
    await client.start(config["bot"]["token"])

import asyncio 
asyncio.run(main())