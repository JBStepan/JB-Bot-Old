import os

import discord
from discord.ext import commands

import bot_settings as settings

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
    await BOT.change_presence(activity=discord.Game(name=rich_presence))

#############
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        BOT.load_extension(f'cogs.{filename[:-3]}')
        print('Loaded cog file ' + filename)

# Run the bot!
BOT.run(TOKEN)
