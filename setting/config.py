import discord 
from discord.ext import commands
from discord import app_commands

import logging

import local


token = local.DISCORD_TOKEN

def handler():
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    return handler

def bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    return bot