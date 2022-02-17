# Pycord
import discord
from discord import activity
from discord.ext import commands
from discord.commands import slash_command

import config

# Cogs
import cogs.mod as mod
import cogs.fun as fun
import cogs.help as help
import cogs.automod as automod

import asyncio

BOT = commands.Bot(command_prefix=config.PREFIX, description="The offical bot of JB\'s Rift Discord server and JB Stepan")
BOT.remove_command('help')
COGS = [mod, fun, help, automod]

@BOT.event
async def on_connect():
    print("\n")
    print("Bot online!")
    print("-----------")

@BOT.event
async def on_command_error(ctx: commands.Context, exception):
    if isinstance(exception, commands.CommandNotFound): 
        em = discord.Embed(title=f"Error!", description=f"Command not found. Please use >help for avaible commands!", color=discord.colour.Color.red()) 
        await ctx.send(embed=em)

async def change_presence():
    await BOT.wait_until_ready()

    while not BOT.is_closed():
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for >'))
        await asyncio.sleep(10)
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for bad words'))
        await asyncio.sleep(10)
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='chat'))
        await asyncio.sleep(10)
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Economy Games"))
        await asyncio.sleep(10)
        await BOT.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Over the Internet"))
        await asyncio.sleep(10)


# Loading cogs
for i in range(len(COGS)):
    if COGS[i].enabled == True:
        COGS[i].setup(BOT)
        print(f"Loading cog: {COGS[i].get_name()}")
    else:
        print(f"Cog {COGS[i].get_name()} not enabled")

BOT.loop.create_task(change_presence())
BOT.run(token=config.TOKEN)