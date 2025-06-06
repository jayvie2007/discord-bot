from dotenv import load_dotenv
from discord.ext import commands

import discord 
import logging

import local
import settings

bot = settings.bot

@bot.slash_command(
  name="first_slash",
  guild_ids=[...]
)

async def first_slash(ctx): 
    await ctx.respond("You executed the slash command!")