import discord
from discord.ext import commands
from discord import app_commands
import json

with open("config.json") as config:
    config = json.load(config)