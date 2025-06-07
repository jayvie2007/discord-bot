from setting import config

bot = config.bot

@bot.slash_command(
  name="first_slash",
  guild_ids=[...]
)

async def first_slash(ctx): 
    await ctx.respond("You executed the slash command!")