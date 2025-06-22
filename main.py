from dotenv import load_dotenv

import discord 
import logging
import local
from discord import app_commands
from setting import config

load_dotenv()

bot = config.bot()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # Global sync
        print(f"Globally synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
        
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(local.default_channel_id)
    await member.send(f"Welcome to the Himalayas {member.name}")
    if channel:
        await channel.send(f"Welcome to the Himalayas {member.mention}!")
    
# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
    
#     bastos_words = local.bastos_words
#     offensive_names = local.offensive_names
#     unathorized_words = local.unathorized_words

#     content_lower = message.content.lower()

#     if any(word in content_lower for word in bastos_words):
#         await message.delete()
#         await message.channel.send(f"{message.author.mention} - HUWAG KANG BASTOS!!!!")

#     elif any(name.lower() in content_lower for name in offensive_names):
#         await message.delete()
#         await message.channel.send(f"{message.author.mention} - BADIIING!!!!")
#         await message.channel.send("http://imgur.com/gallery/YiMUiop")    
    
#     elif any(name.lower() in content_lower for name in unathorized_words):
#         await message.delete()
#         await message.channel.send(f"{message.author.mention} Do you have NPASS")
#         await message.channel.send("https://i.imgur.com/UdTWT64.jpeg")    
        
#     await bot.process_commands(message)
  
    
# !message #channel_name #message can also mention
@bot.command()
async def message(ctx, channel: discord.TextChannel, *, message: str):
    await ctx.message.delete()
    await channel.send(message)
    

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


@bot.command()
async def announcement(ctx, channel: discord.TextChannel, *, message: str):
    allowed = discord.AllowedMentions(everyone=True, users=True, roles=True)
    file = discord.File("images/triple.png", filename="triple.png")
    await channel.send(message, allowed_mentions=allowed, file=file)
    
    
@bot.tree.command(name="message", description="Send a custom message to the channel")
async def message(interaction: discord.Interaction, *, content: str):
    await interaction.response.send_message(content)
    

@bot.tree.command(name="hello", description="Say hello!")
async def helloTest(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.name}!")

bot.run(local.DISCORD_TOKEN, log_handler=config.handler(), log_level=logging.DEBUG)