import pycord
from pycord.ext import commands

import config

BOT = commands.Bot(command_prefix=config.PREFIX, description="A bot for me and my friends\' Discords.")
COGS = []

@BOT.event
async def on_connect():
    print("\n")
    print("Bot online!")

# Loading cogs
for i in range(len(COGS)):
    COGS[i].setup(BOT)

BOT.run(token=config.TOKEN)