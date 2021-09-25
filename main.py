# Pycord
from os import name
import discord
from discord.ext import commands

import config

# Cogs
import cogs.user as users
import cogs.econ as econ
import cogs.member_config as verify
import cogs.mod as mod

BOT = commands.Bot(command_prefix=config.PREFIX, description="The offical bot of JB\'s Rift Discord server and JB Stepan")
COGS = [users, econ, verify, mod]

@BOT.event
async def on_connect():
    print("\n")
    print("Bot online!")
    await BOT.change_presence(activity=discord.Game(name=' for $'))

# Loading cogs
for i in range(len(COGS)):
    COGS[i].setup(BOT)
    print(f"Loading cog: {COGS[i].get_name()}")

BOT.run(token=config.TOKEN)