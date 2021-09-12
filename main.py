import os
import discord
from discord.ext import commands

import bot_settings as settings
import web_dashboard.web_dash as webdash

# Discord variables
TOKEN = settings.token
BOT = commands.Bot(command_prefix=settings.command_prefix)
BOT.remove_command('help')
rich_presence = f'Listening for {settings.command_prefix}'

# Client events
@BOT.event
async def on_ready():
    print('\n')
    print('Bot as started')
    #webdash.start_dash(BOT)


#############
for filename in os.listdir('C:/Users/wayne/Desktop/Jakob2/JB Programs/JB Bot/cogs'):
    if filename.endswith('.py'):
        BOT.load_extension(f'cogs.{filename[:-3]}')
        print('Loaded cog file ' + filename)

# Run the bot!
BOT.run(TOKEN)