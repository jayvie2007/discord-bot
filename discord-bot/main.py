from dotenv import load_dotenv
from discord.ext import commands

import discord 
import logging

import local

load_dotenv()
token = local.DISCORD_TOKEN

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# This is the start bot command for discord !hello or !role
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Himalayas bot is now running")
    
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the Himalayas {member.name}")
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    bastos_words = local.bastos_words
    offensive_names = local.offensive_names
    unathorized_words = local.unathorized_words

    content_lower = message.content.lower()

    if any(word in content_lower for word in bastos_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention} - HUWAG KANG BASTOS!!!!")

    elif any(name.lower() in content_lower for name in offensive_names):
        await message.delete()
        await message.channel.send(f"{message.author.mention} - BADIIING!!!!")
        await message.channel.send("http://imgur.com/gallery/YiMUiop")    
    
    elif any(name.lower() in content_lower for name in unathorized_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention} Do you have NPASS")
        await message.channel.send("https://i.imgur.com/UdTWT64.jpeg")    
        
    await bot.process_commands(message)
    
    
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}")
    
@bot.command()
async def message(ctx, *, message:str):
    await ctx.channel.send(message)    
    
    
@bot.command()
async def channel_message(ctx, channel: discord.TextChannel, *, message: str):
    await channel.send(message)


@bot.command()
async def channel_message_everyone(ctx, channel: discord.TextChannel, *, message: str):
    # Allow everyone, roles, and user mentions to be parsed and pinged
    allowed = discord.AllowedMentions(everyone=True, users=True, roles=True)
    await channel.send(message, allowed_mentions=allowed)


@bot.command()
async def rules(ctx):
    rules = local.rules
    await ctx.send(rules)


@bot.command()
async def assign(ctx, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {role}" )
    else:
        await ctx.send(f"no roles assigned {ctx.author.mention}")


@bot.command()
async def remove_role(ctx, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} {role} role is now removed" )
    else:
        await ctx.send(f"no roles assigned {ctx.author.mention}")



bot.run(token, log_handler=handler, log_level=logging.DEBUG)