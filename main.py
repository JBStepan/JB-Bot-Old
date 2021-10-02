# Pycord
import discord
from discord.ext import commands

import config

# Cogs
import cogs.user as users
import cogs.econ as econ
import cogs.member_config as verify
import cogs.mod as mod
import cogs.help as help
import cogs.automod as automod

import asyncio

BOT = commands.Bot(command_prefix=config.PREFIX, description="The offical bot of JB\'s Rift Discord server and JB Stepan")
BOT.remove_command('help')
COGS = [users, econ, verify, mod, help, automod]

@BOT.event
async def on_connect():
    print("\n")
    print("Bot online!")

async def change_presence():
    await BOT.wait_until_ready()

    while not BOT.is_closed():
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for $'))
        await asyncio.sleep(10)
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for bad words'))
        await asyncio.sleep(10)
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='chat'))
        await asyncio.sleep(10)
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='JB Music'))
        await asyncio.sleep(10)

# Loading cogs
for i in range(len(COGS)):
    COGS[i].setup(BOT)
    print(f"Loading cog: {COGS[i].get_name()}")

BOT.loop.create_task(change_presence())
BOT.run(token=config.TOKEN)