from dotenv import load_dotenv
from discord.ext import commands

import discord 
import logging

import local
import slash_command


token = local.DISCORD_TOKEN

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# This is the start bot command for discord !hello or !role
bot = commands.Bot(command_prefix='!', intents=intents)