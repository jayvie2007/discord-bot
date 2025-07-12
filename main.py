from dotenv import load_dotenv

import discord 
import logging
import local
from discord import app_commands, Message
from setting import config

from datetime import datetime, timedelta
import pytz
import asyncio

load_dotenv()

bot = config.bot()

def has_allowed_role():
    async def predicate(interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        return any(role_id in user_roles for role_id in local.ALLOWED_ROLE_IDS)
    return app_commands.check(predicate)

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
async def update_rules(ctx):
    channel = ctx.channel
    message_id = 1378946017042501751
    try:
        message: Message = await channel.fetch_message(message_id)
        await message.edit(content=local.rules)
        await ctx.send("✅ Rules updated successfully.")
    except Exception as e:
        await ctx.send(f"⚠️ Could not update rules: {e}")


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
    

@has_allowed_role()
@bot.tree.command(name="message", description="Send a custom message to the channel")
@app_commands.describe(
    message="The message to send",
)
async def send_message(
    interaction: discord.Interaction,
    message: str,
):

    await interaction.channel.send(message)
    await interaction.response.send_message(f"✅ Sent message to this channel", ephemeral=True)


@has_allowed_role()
@bot.tree.command(name="reply", description="Send a reply to a custom message to the channel")
@app_commands.describe(
    message_id="ID of the message",  # <-- This does NOT match any parameter!
    reply="Your message to reply"
)
async def send_reply(
    interaction: discord.Interaction,
    message_id: str,
    reply: str
):
    await interaction.response.defer(ephemeral=True)
    try:
        msg = await interaction.channel.fetch_message(int(message_id))
        await msg.reply(reply)
        await interaction.followup.send("✅ Replied to the message!", ephemeral=True)
    except discord.NotFound:
        await interaction.followup.send("❌ Message not found.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ Missing permissions to read or reply.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Unexpected error: {e}", ephemeral=True)
        
        
@has_allowed_role()
@bot.tree.command(name="countdown", description="Countdown")
async def countdown(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    target_timezone = pytz.timezone('Asia/Manila')
    target_time = target_timezone.localize(datetime(datetime.now().year, 7, 15, 1, 0, 0))  # July 15, 1:00 AM
    # target_time = target_timezone.localize(datetime(datetime.now().year, 7, 11, 15, 5, 0))  # July 15, 1:00 AM

    guild = interaction.guild
    crew_role = discord.utils.get(guild.roles, name="The Crew")
    syndicate_role = discord.utils.get(guild.roles, name="Syndicate")
    autobots_role = discord.utils.get(guild.roles, name="Autobots")

    now = datetime.now(target_timezone)
    if now >= target_time:
        await interaction.response.send_message("⏰ Already done!")
        return

    embed = discord.Embed(
        # title="📆 Test",
        title="📆 Countdown to Automation Fest - July 15, 1:00 AM",
        description="Calculating time remaining...",
        color=discord.Color.blue()
    )

    countdown_message = await interaction.channel.send(embed=embed)

    async def countdown_loop():
        while True:
            now = datetime.now(target_timezone)
            remaining = target_time - now

            if remaining.total_seconds() <= 0:
                embed.description = "🎉 Automation Fest has arrived! Go check Steam!!"
                # embed.description = "🎉 Test"
                embed.color = discord.Color.green()
                await countdown_message.edit(embed=embed)
                # await interaction.channel.send(f"{autobots_role.mention} 🚀 Test!")
                await interaction.followup.send(f"{crew_role.mention} {syndicate_role.mention} 🚀 Automation Fest has started!")
                break

            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_str = f"{days}d {hours}h {minutes}m {seconds}s remaining"
            embed.description = f"🕐 {time_str}"
            await countdown_message.edit(embed=embed)
            await asyncio.sleep(1)

    # Start the countdown loop in background
    bot.loop.create_task(countdown_loop())

@send_message.error
async def send_message_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)
    
bot.run(local.DISCORD_TOKEN, log_handler=config.handler(), log_level=logging.DEBUG)