import os

import discord
from discord.ext import commands

# Discord variables
TOKEN = 'NzkwNzI5NTI4ODM3NTM3ODEy.X-E2Qg.0abQ5tGW5T2OmjYdXF-RkUp1lRw'
BOT = commands.Bot(command_prefix='$')
BOT.remove_command('help')
rich_presence = 'Listening for $'

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
