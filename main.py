import nextcord
import bot_token
import os
import json

from nextcord.ext import commands

os.chdir("E:\Dev\Py\Herobrine")

bot = commands.Bot(command_prefix="h.")

@bot.event
async def on_ready():
    print("Bot ready!")
    
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')
    
bot.run(bot_token.TOKEN)