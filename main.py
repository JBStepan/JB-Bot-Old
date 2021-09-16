# Pycord
import pycord
from pycord.ext import commands

import config

# Cogs
import cogs.user as users
import cogs.mod as mod

BOT = commands.Bot(command_prefix=config.PREFIX, description="A bot for me and my friends\' Discords.")
COGS = [users, mod]

@BOT.event
async def on_connect():
    print("\n")
    print("Bot online!")

# Loading cogs
for i in range(len(COGS)):
    COGS[i].setup(BOT)
    print(f"Loading cog: {COGS[i].get_name()}")

BOT.run(token=config.TOKEN)