# Pycord
import discord
from discord.ext import commands

import config

# Cogs
import cogs.user as users
import cogs.mod as mod
import cogs.econ as econ

BOT = commands.Bot(command_prefix=config.PREFIX, description="The offical bot of JB\'s Rift Discord server and JB Stepan")
COGS = [users, mod, econ]

@BOT.event
async def on_connect():
    print("\n")
    print("Bot online!")

# Loading cogs
for i in range(len(COGS)):
    COGS[i].setup(BOT)
    print(f"Loading cog: {COGS[i].get_name()}")

BOT.run(token=config.TOKEN)